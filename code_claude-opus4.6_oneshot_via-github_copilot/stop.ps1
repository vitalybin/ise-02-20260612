# Smart-Home-Verwaltung - Stop
Write-Host "=== Smart-Home-Verwaltung stoppen ===" -ForegroundColor Yellow

docker compose down

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Container erfolgreich gestoppt." -ForegroundColor Green
    Write-Host ""
    Write-Host "Hinweis: Datenbankdaten bleiben im Volume 'smart-home-db-volume' erhalten."
    Write-Host "Zum vollstaendigen Loeschen: docker compose down -v"
} else {
    Write-Host "FEHLER beim Stoppen!" -ForegroundColor Red
}
