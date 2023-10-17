import anyio
import click
from pipelines.commands.groups.connectors.connectors import connectors
from pipelines.contexts import ConnectorContext
from pipelines.format import run_connectors_format_pipelines
from pipelines.utils import DaggerPipelineCommand


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
        run_connectors_format_pipelines,
        connectors_contexts,
        ctx.obj["ci_git_user"],
        ctx.obj["ci_github_access_token"],
        ctx.obj["git_branch"],
        ctx.obj["is_local"],
        ctx.obj["execute_timeout"],
    )

    return True
