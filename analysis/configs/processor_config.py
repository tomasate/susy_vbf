class ProcessorConfig:
    """
    Attributes:
    -----------
        goldenjson:
        hlt_paths:
        object_selection:
        event_selection:
    """
    def __init__(
        self, goldenjson, hlt_paths, object_selection, event_selection, histogram_config
    ):
        self.goldenjson = goldenjson
        self.hlt_paths = hlt_paths
        self.object_selection = object_selection
        self.event_selection = event_selection
        self.histogram_config = histogram_config