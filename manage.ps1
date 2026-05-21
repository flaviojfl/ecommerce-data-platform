# manage.ps1 - Comandos de conveniência para gerenciar o ambiente
# Uso: .\manage.ps1 <comando>
#   up       - sobe todos os serviços
#   down     - derruba todos os serviços
#   restart  - reinicia tudo
#   status   - mostra status dos containers
#   logs     - mostra logs (ex: .\manage.ps1 logs mysql)
#   clean    - derruba e remove volumes (CUIDADO: apaga dados)

param(
    [Parameter(Mandatory=$true)]
    [string]$Command,

    [Parameter(Mandatory=$false)]
    [string]$Service
)

switch ($Command) {
    "up" {
        Write-Host "Subindo todos os servicos..." -ForegroundColor Green
        docker compose up -d
    }
    "down" {
        Write-Host "Derrubando servicos..." -ForegroundColor Yellow
        docker compose down
    }
    "restart" {
        Write-Host "Reiniciando servicos..." -ForegroundColor Cyan
        docker compose down
        docker compose up -d
    }
    "status" {
        docker compose ps
    }
    "logs" {
        if ($Service) {
            docker compose logs -f $Service
        } else {
            docker compose logs -f
        }
    }
    "clean" {
        Write-Host "ATENCAO: isso vai apagar todos os dados (volumes)!" -ForegroundColor Red
        $confirm = Read-Host "Digite 'sim' para confirmar"
        if ($confirm -eq "sim") {
            docker compose down -v
            Write-Host "Ambiente limpo." -ForegroundColor Green
        } else {
            Write-Host "Cancelado." -ForegroundColor Yellow
        }
    }
    default {
        Write-Host "Comando desconhecido: $Command" -ForegroundColor Red
        Write-Host "Comandos disponiveis: up, down, restart, status, logs, clean"
    }
}