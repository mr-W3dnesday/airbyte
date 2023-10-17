import anyio
import click
from pipelines.cli.dagger_pipeline_command import DaggerPipelineCommand
from pipelines.pipeline.connectors.commands import connectors
from pipelines.pipeline.connectors.context import ConnectorContext
from pipelines.pipeline.connectors.format.steps import run_connector_format_pipeline
from pipelines.pipeline.connectors.pipeline import run_connectors_pipelines


@connectors.command(name="format", cls=DaggerPipelineCommand, help="Autoformat connector code.")
@click.pass_context
def format_code(ctx: click.Context) -> bool:
    connectors_contexts = [
        ConnectorContext(
            pipeline_name=f"Format connector {connector.technical_name}",
            connector=connector,
            is_local=ctx.obj["is_local"],
            git_branch=ctx.obj["git_branch"],
            git_revision=ctx.obj["git_revision"],
            ci_report_bucket=ctx.obj["ci_report_bucket_name"],
            report_output_prefix=ctx.obj["report_output_prefix"],
            use_remote_secrets=ctx.obj["use_remote_secrets"],
            gha_workflow_run_url=ctx.obj.get("gha_workflow_run_url"),
            dagger_logs_url=ctx.obj.get("dagger_logs_url"),
            pipeline_start_timestamp=ctx.obj.get("pipeline_start_timestamp"),
            ci_context=ctx.obj.get("ci_context"),
            ci_gcs_credentials=ctx.obj["ci_gcs_credentials"],
            ci_git_user=ctx.obj["ci_git_user"],
            ci_github_access_token=ctx.obj["ci_github_access_token"],
            pull_request=ctx.obj.get("pull_request"),
            should_save_report=False,
        )
        for connector in ctx.obj["selected_connectors_with_modified_files"]
    ]

    anyio.run(
        run_connectors_pipelines,
        connectors_contexts,
        run_connector_format_pipeline,
        "Format connectors pipeline",
        ctx.obj["concurrency"],
        ctx.obj["dagger_logs_path"],
        ctx.obj["execute_timeout"],
    )

    return True
