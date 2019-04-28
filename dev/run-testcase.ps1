$validTargets = @("lexer", "parser")
$target = $args[0]

if($target -and $validTargets.Contains($target)){
    $cache = Get-Location
    Set-Location -Path "../lib/GenshiBASIC"
    Invoke-Expression -Command "python -m unittest tests.test_$target"
    Set-Location -Path $cache
} else{
    Write-Host("Invalid target.")
    Write-Host("Possible targets:")
    for ($i = 0; $i -lt $validTargets.Count; $i++) {
        Write-Host("   " + $validTargets[$i]);
    }
}

# Run a single test:
# python -m unittest tests.test_lexer.Test_Lexer.test_tokens_MissingQuotation