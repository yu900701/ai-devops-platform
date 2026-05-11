from dataclasses import dataclass
from pathlib import Path


@dataclass
class AnalysisResult:
    category: str
    summary: str
    possible_causes: list[str]
    suggested_fixes: list[str]
    related_files: list[str]
    next_commands: list[str]


class CILogAnalyzer:
    def analyze(self, log_text: str) -> AnalysisResult:
        lower_log = log_text.lower()

        if "passed" in lower_log and "failed" not in lower_log and "error" not in lower_log:
            return AnalysisResult(
                category="CI Passed",
                summary="CI 測試已通過，沒有偵測到失敗訊息。",
                possible_causes=[
                    "目前 CI log 顯示測試成功。",
                ],
                suggested_fixes=[
                    "不需要修復。",
                ],
                related_files=[
                    "tests/test_api.py",
                    "app/main.py",
                ],
                next_commands=[
                    "pytest",
                ],
            )
            
        if "modulenotfounderror" in lower_log or "no module named" in lower_log:
            return AnalysisResult(
                category="Python Import Error",
                summary="CI 失敗原因可能是 Python module import 路徑錯誤。",
                possible_causes=[
                    "測試檔案中的 import path 不正確。",
                    "缺少 __init__.py，導致資料夾沒有被視為 Python package。",
                    "pytest 執行位置不在 project root。",
                    "PYTHONPATH 沒有包含專案根目錄。",
                ],
                suggested_fixes=[
                    "確認 test 檔案使用 from app.main import app。",
                    "確認 app/ 與 tests/ 中有 __init__.py。",
                    "從專案根目錄執行 pytest。",
                    "必要時在 CI 中設定 PYTHONPATH=.",
                ],
                related_files=[
                    "tests/test_api.py",
                    "app/main.py",
                    "app/__init__.py",
                    "tests/__init__.py",
                    ".github/workflows/ci-cd.yml",
                    "cicd/jenkins/Jenkinsfile",
                ],
                next_commands=[
                    "pytest",
                    "PYTHONPATH=. pytest",
                    "tree app tests",
                ],
            )

        if "failed" in lower_log and "assert" in lower_log:
            return AnalysisResult(
                category="Test Assertion Failure",
                summary="CI 失敗原因是測試 assertion 未通過。",
                possible_causes=[
                    "測試預期結果與 API 實際回傳不一致。",
                    "API 行為被修改，但測試尚未更新。",
                    "測試資料或 status code 設定錯誤。",
                ],
                suggested_fixes=[
                    "查看 pytest 失敗位置，確認 expected value 與 actual value。",
                    "若 API 行為正確，更新 test case。",
                    "若 test case 正確，修正 app 程式邏輯。",
                ],
                related_files=[
                    "tests/test_api.py",
                    "app/main.py",
                ],
                next_commands=[
                    "pytest -vv",
                    "pytest tests/test_api.py -vv",
                ],
            )

        if "no matching distribution found" in lower_log:
            return AnalysisResult(
                category="Python Dependency Error",
                summary="CI 失敗原因可能是 requirements.txt 中有不存在或版本錯誤的套件。",
                possible_causes=[
                    "套件名稱拼錯。",
                    "指定的版本不存在。",
                    "Python 版本與套件版本不相容。",
                ],
                suggested_fixes=[
                    "檢查 requirements.txt 中的套件名稱。",
                    "確認 CI 使用的 Python 版本。",
                    "移除或更正錯誤的版本限制。",
                ],
                related_files=[
                    "app/requirements.txt",
                    ".github/workflows/ci-cd.yml",
                    "cicd/jenkins/Jenkinsfile",
                ],
                next_commands=[
                    "pip install -r app/requirements.txt",
                    "python --version",
                    "pip index versions <package-name>",
                ],
            )

        if "docker build" in lower_log and ("error" in lower_log or "failed" in lower_log):
            return AnalysisResult(
                category="Docker Build Failure",
                summary="CI 失敗原因可能發生在 Docker image build 階段。",
                possible_causes=[
                    "Dockerfile COPY 路徑錯誤。",
                    "requirements.txt 路徑錯誤。",
                    "pip install 失敗。",
                    "CMD 或 WORKDIR 設定錯誤。",
                ],
                suggested_fixes=[
                    "確認 docker build 的 context 是專案根目錄。",
                    "確認 Dockerfile 中 COPY app/requirements.txt . 是否正確。",
                    "本地執行 docker build 重現錯誤。",
                ],
                related_files=[
                    "docker/app.Dockerfile",
                    "app/requirements.txt",
                    ".dockerignore",
                ],
                next_commands=[
                    "docker build -f docker/app.Dockerfile -t ai-devops-app:test .",
                    "docker run -p 8000:8000 ai-devops-app:test",
                ],
            )

        if "permission denied" in lower_log and "docker" in lower_log:
            return AnalysisResult(
                category="Docker Permission Error",
                summary="CI 失敗原因可能是 Jenkins 使用者沒有 Docker 權限。",
                possible_causes=[
                    "jenkins 使用者不在 docker group。",
                    "Docker daemon 沒有啟動。",
                    "WSL 中 Docker Desktop integration 未啟用。",
                ],
                suggested_fixes=[
                    "將 jenkins 使用者加入 docker group。",
                    "重啟 Jenkins。",
                    "確認 docker ps 在 Jenkins pipeline 中可執行。",
                ],
                related_files=[
                    "cicd/jenkins/Jenkinsfile",
                ],
                next_commands=[
                    "sudo usermod -aG docker jenkins",
                    "sudo service jenkins restart",
                    "docker ps",
                ],
            )

        if "denied" in lower_log and ("ghcr.io" in lower_log or "docker push" in lower_log):
            return AnalysisResult(
                category="Container Registry Authentication Error",
                summary="CI 失敗原因可能是推送 image 到 GHCR 時驗證失敗。",
                possible_causes=[
                    "GHCR token 錯誤或過期。",
                    "PAT 缺少 write:packages 權限。",
                    "docker login 使用的 username 或 token 錯誤。",
                    "image namespace 不正確。",
                ],
                suggested_fixes=[
                    "檢查 Jenkins / GitHub Actions 中的 GHCR credentials。",
                    "確認 PAT 有 read:packages 與 write:packages。",
                    "確認 image 名稱符合 ghcr.io/<username>/<image>:<tag>。",
                ],
                related_files=[
                    "cicd/jenkins/Jenkinsfile",
                    ".github/workflows/ci-cd.yml",
                ],
                next_commands=[
                    "docker login ghcr.io",
                    "docker push ghcr.io/<username>/ai-devops-app:<tag>",
                ],
            )

        return AnalysisResult(
            category="Unknown CI Failure",
            summary="目前無法用規則明確判斷錯誤類型，需要人工查看 log。",
            possible_causes=[
                "錯誤類型尚未被 Agent 規則涵蓋。",
                "log 資訊不足。",
                "錯誤發生在外部服務或環境設定。",
            ],
            suggested_fixes=[
                "查看完整 CI log。",
                "增加 Agent 規則。",
                "若之後串接 LLM，可以交由 LLM 做更彈性的分析。",
            ],
            related_files=[
                ".github/workflows/ci-cd.yml",
                "cicd/jenkins/Jenkinsfile",
            ],
            next_commands=[
                "pytest -vv",
                "docker build -f docker/app.Dockerfile -t ai-devops-app:test .",
                "docker ps",
            ],
        )


def load_log_file(log_file: str) -> str:
    path = Path(log_file)

    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {log_file}")

    return path.read_text(encoding="utf-8", errors="ignore")