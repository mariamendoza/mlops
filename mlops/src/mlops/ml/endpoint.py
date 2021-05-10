from mlops.ml.pipeline import MlPipeline

class MlEndpoint():

    def __init__(self, workspace):
        self.workspace = workspace

    def build_pipeline(self, config):
        self.config = config
        self.pipeline = MlPipeline(self.workspace).from_config(self.config)

    def deploy(self):
        pipeline_endpoint_name = self.config.get("endpoint_name")
        pipeline_endpoint_version = self.config.get("endpoint_version")
        pipeline_endpoint_desc = self.config.get("endpoint_desc")

        published_pipeline = self.pipeline.publish(
            name=pipeline_endpoint_name, 
            description=pipeline_endpoint_desc, 
            version=pipeline_endpoint_version,
            continue_on_step_failure=False)
        
        self.url = published_pipeline.endpoint
