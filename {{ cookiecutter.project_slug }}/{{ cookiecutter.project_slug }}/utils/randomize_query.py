from .read_data import ReadData

class RandomizeQuery:

    def __init__(self, original_query, sample_size, random_state: int = 42) -> None:
        self.original_query = original_query.lower()
        self.sample_size = sample_size
        self.random_state = random_state

    def randomize_samples(self, verbose: bool = False) -> str:

        # Format counting queries
        if 'union all' in self.original_query:
            queries = self.original_query.split('union all')
            total_queries = len(queries)
            count_query = 'union all\n'.join([''.join(['select \n\tcount(*) AS count_\nfrom', q.split('from')[-1]]) for q in queries])
        else:
            queries = [self.original_query]
            total_queries = 1
            count_query = ''.join(['select \n\tcount(*) AS count_\nfrom', self.original_query.split('from')[-1]])
        
        # Format original query with random sample selection
        if verbose:
            print('Counting samples in databases ...')
            print(count_query)

        sample_sizes = self.__calc_sample_sizes(count_query=count_query, total_queries=total_queries)
        new_queries = []
        for q,s in zip(queries, sample_sizes):
            q = q.lower().split('union all')[0].strip('\n')
            new_query = f"{q}\norder by random({self.random_state})\nlimit {s}"
            new_queries.append(new_query)
        
        if total_queries == 1:
            return new_queries[0].strip('\n')
        else:
            return '\nunion all\n'.join(new_queries).strip('\n')
        
    def __calc_sample_sizes(self, count_query: str, total_queries: int) -> list:
        if self.sample_size <= 0:
            raise ValueError("The number can't be lower than 0")
        elif self.sample_size < 1:
            df_count = ReadData().from_impala(count_query, verbose=False)
            sample_sizes = [int(val) for val in (df_count.count_ * self.sample_size).values]
        else:
            decimal_part = self.sample_size % 1
            if abs(decimal_part-0) < 0.00000001:
                sample_sizes = [self.sample_size] * total_queries
            else:
                raise ValueError("The sample size cannot be an integer with decimals")
            
        return sample_sizes