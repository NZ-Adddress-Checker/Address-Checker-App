param(
    [string]$Owner = "NZ-Adddress-Checker",
    [string]$Repo = "Address-Checker-App",
    [string]$Branch = "practice",
    [string]$CommitSha = "",
    [int]$PerPage = 30,
    [int]$PollSeconds = 20,
    [switch]$Watch
)

$ErrorActionPreference = "Stop"

function Get-ApiHeaders {
    $headers = @{
        "Accept" = "application/vnd.github+json"
        "X-GitHub-Api-Version" = "2022-11-28"
    }

    if ($env:GH_TOKEN) {
        $headers["Authorization"] = "Bearer $($env:GH_TOKEN)"
    }

    return $headers
}

function Get-Runs {
    param(
        [string]$Owner,
        [string]$Repo,
        [string]$Branch,
        [int]$PerPage,
        [string]$CommitSha
    )

    $url = "https://api.github.com/repos/$Owner/$Repo/actions/runs?branch=$Branch&per_page=$PerPage"
    $response = Invoke-RestMethod -Uri $url -Headers (Get-ApiHeaders)

    $runs = @($response.workflow_runs)
    if ($CommitSha) {
        $runs = @($runs | Where-Object { $_.head_sha -like "$CommitSha*" })
    }

    return $runs
}

function Show-Runs {
    param([array]$Runs)

    if (-not $Runs -or $Runs.Count -eq 0) {
        Write-Output "No workflow runs found for current filter."
        return
    }

    $Runs |
        Select-Object name, status, conclusion, id, html_url |
        Sort-Object name |
        Format-Table -AutoSize
}

if (-not $CommitSha) {
    try {
        $CommitSha = (git rev-parse --short HEAD).Trim()
    } catch {
        $CommitSha = ""
    }
}

Write-Output "Using repo: $Owner/$Repo"
Write-Output "Branch: $Branch"
if ($CommitSha) {
    Write-Output "Commit filter: $CommitSha"
}
if ($env:GH_TOKEN) {
    Write-Output "Auth: GH_TOKEN detected (higher API limits)."
} else {
    Write-Output "Auth: no GH_TOKEN detected (unauthenticated API limits)."
}

while ($true) {
    try {
        $runs = Get-Runs -Owner $Owner -Repo $Repo -Branch $Branch -PerPage $PerPage -CommitSha $CommitSha
    } catch {
        Write-Error "GitHub API request failed. If this is rate limiting, set GH_TOKEN and retry. Details: $($_.Exception.Message)"
        exit 1
    }

    Show-Runs -Runs $runs

    if (-not $Watch) {
        break
    }

    $inProgress = @($runs | Where-Object { $_.status -ne "completed" }).Count
    if ($inProgress -eq 0) {
        Write-Output "ALL_DONE"
        break
    }

    Write-Output "STILL_RUNNING - polling again in $PollSeconds seconds..."
    Start-Sleep -Seconds $PollSeconds
}
