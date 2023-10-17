#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#


from pipelines.actions import environments
from pipelines.helpers.utils import get_exec_result
from pipelines.models.steps import StepResult
from pipelines.pipelines.models.steps import GradleTask


class FormatConnectorCode(GradleTask):
    """
    A step to format a Java connector code.
    """

    title = "Format connector code"
    gradle_task_name = "format"

    async def _run(self) -> StepResult:
        result = await super()._run()
        return StepResult(
            self,
            result.status,
            stderr=result.stderr,
            stdout=result.stdout,
            output_artifact=result.output_artifact.directory(str(self.context.connector.code_directory)),
        )
