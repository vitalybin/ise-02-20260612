# Smart-Home-Verwaltung - Start
Write-Host "=== Smart-Home-Verwaltung starten ===" -ForegroundColor Green
Write-Host ""

# Pruefen ob Docker laeuft
try {
    docker info 2>&1 | Out-Null
} catch {
    Write-Host "FEHLER: Docker ist nicht gestartet!" -ForegroundColor Red
    Write-Host "Bitte starten Sie Docker Desktop und versuchen Sie es erneut."
    exit 1
}

# Container starten
Write-Host "Container werden gebaut und gestartet..."
docker compose up --build -d

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=== Anwendung erfolgreich gestartet ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Web-UI:     http://localhost:5000" -ForegroundColor Cyan
    Write-Host "  Datenbank:  localhost:5431" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Standard-Zugaenge:" -ForegroundColor Yellow
    Write-Host "    admin     / admin      (ADMIN)"
    Write-Host "    techniker / techniker  (TECHNIKER)"
    Write-Host "    viewer    / viewer     (VIEWER)"
    Write-Host ""
    Write-Host "  Zum Stoppen: .\stop.ps1"
} else {
    Write-Host "FEHLER beim Starten der Container!" -ForegroundColor Red
    docker compose logs
}
