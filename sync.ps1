# 個別プロジェクト用の一撃同期スクリプト
$ErrorActionPreference = "Stop"

# 1. 変更をすべて追加
Write-Host "[Git] Adding changes..."
git add .

# 2. 変更がある場合のみコミット
$Status = git status --porcelain
if ($Status) {
    $Message = "Auto update: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    Write-Host "[Git] Committing changes: $Message"
    git commit -m $Message
} else {
    Write-Host "[Git] No changes to commit."
}

# 3. GitHubへ送信
$Branch = git branch --show-current
Write-Host "[Git] Pushing to origin ($Branch)..."
git push origin $Branch

Write-Host "`n--- 同期が完了しました！ ---"
