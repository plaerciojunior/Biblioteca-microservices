using System.Net.Http.Json;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace BibliotecaMicroservice.Handlers
{
    public class AnalyticsHandler
    {
        private readonly HttpClient _httpClient;

        public AnalyticsHandler(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<DashboardDataDto?> GetDashboardDataAsync()
        {
            try { return await _httpClient.GetFromJsonAsync<DashboardDataDto>("http://localhost:5000/analytics/dashboard"); }
            catch { return null; }
        }
    }

    public class DashboardDataDto
    {
        public int total_alugueis { get; set; }
        public int usuarios_ativos { get; set; }
        public int emprestimos_atrasados { get; set; }
        public double tempo_medio_retorno { get; set; }
        public Dictionary<string, int> alugueis_por_mes { get; set; } = new();
        public Dictionary<string, double> lucro_por_mes { get; set; } = new();
    }
}