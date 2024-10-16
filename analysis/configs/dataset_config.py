class DatasetConfig:
    """
    Container for information about a dataset.

    Attributes:
    -----------
        name: 
            short name of the dataset
        process: 
            physical process class (used as a key to accumulate datasets in postprocessing)
        query: 
            Dataset DAS query
        year: 
            year of the dataset
        is_mc: 
            Is the dataset MC?
        xsec: 
            dataset cross section
        partitions: 
            number of partitions when building the dataset
    """
    def __init__(
        self,
        name: str,
        process: str,
        query: str,
        year: str,
        is_mc: str,
        xsec: float,
        partitions: int,
    ) -> None:

        self.name = name
        self.process = process
        self.query = query
        self.year = year
        self.is_mc = is_mc
        self.xsec = xsec
        self.partitions = partitions

    def __repr__(self):
        return f"DatasetConfig({self.name}, {self.year})"