$envFilePath = ".\.env"

if (Test-Path $envFilePath) {
    Write-Host "Looking for .env file at path: $envFilePath"
    Write-Host "Found .env file, reading content..."

    $lines = Get-Content $envFilePath
    $variables = @{}

    foreach ($line in $lines) {
        if ($line -notmatch '^\s*#' -and $line -match '^export\s+([^=\s]+)=([^=\s]+)') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()

            foreach ($var in $variables.Keys) {
                $value = $value -replace "\$\{$var\}", $variables[$var]
            }

            [System.Environment]::SetEnvironmentVariable($key, $value, [System.EnvironmentVariableTarget]::User)
            $variables[$key] = $value
        }
    }

    Write-Host "Environment variables set:"
    foreach ($key in $variables.Keys) {
        Write-Host "$key = $($variables[$key])"
    }
} else {
    Write-Host "The .env file is not found in the directory."
}
