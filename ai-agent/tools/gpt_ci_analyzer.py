import os
from pathlib import Path

from openai import OpenAI

from tools.ci_log_analyzer import AnalysisResult


class GPTCIAnalyzer:
    def __init__(
        self,
        model: str = "gpt-5.5",
        prompt_file: str = "ai-agent/prompts/ci_failure_prompt.txt",
    ) -> None:
        self.model = model
        self.prompt_file = prompt_file
        self.client = OpenAI()

    def _load_prompt(self) -> str:
        path = Path(self.prompt_file)

        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {self.prompt_file}")

        return path.read_text(encoding="utf-8")

    def _truncate_log(self, log_text: str, max_chars: int = 12000) -> str:
        if len(log_text) <= max_chars:
            return log_text

        return log_text[-max_chars:]

    def generate_report(
        self,
        log_text: str,
        rule_result: AnalysisResult,
        project_context: str | None = None,
    ) -> str:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not set.")

        system_prompt = self._load_prompt()
        truncated_log = self._truncate_log(log_text)

        context = project_context or """
專案背景：
- 這是一個 FastAPI App。
- 測試使用 pytest。
- CI/CD 流程可能由 Jenkins 或 GitHub Actions 執行。
- Docker image 會被 build 並 push 到 GHCR。
- GitOps Repo 會被更新 image tag。
- Argo CD 會根據 GitOps Repo 部署到 Kubernetes。
"""

        user_input = f"""
以下是 CI failure 的資料。

## Project Context

{context}

## Rule-based Analyzer Result

Category:
{rule_result.category}

Summary:
{rule_result.summary}

Possible Causes:
{chr(10).join(["- " + item for item in rule_result.possible_causes])}

Suggested Fixes:
{chr(10).join(["- " + item for item in rule_result.suggested_fixes])}

Related Files:
{chr(10).join(["- " + item for item in rule_result.related_files])}

Suggested Next Commands:
{chr(10).join(["- " + item for item in rule_result.next_commands])}

## CI Log

```text
{truncated_log}
"""
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
        )

        return response.output_text