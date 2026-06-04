using System.Net.Http.Json;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace BibliotecaMicroservice.Handlers
{
    public class LoanHandler
    {
        private readonly HttpClient _httpClient;

        public LoanHandler(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<(bool Success, string Message)> CreateLoanAsync(int userId, int bookId)
        {
            var request = new { usuario_id = userId, livro_id = bookId };
            var response = await _httpClient.PostAsJsonAsync("http://localhost:5000/loans", request);
            
            if (response.IsSuccessStatusCode)
                return (true, "Empréstimo realizado");
                
            var error = await response.Content.ReadFromJsonAsync<Dictionary<string, string>>();
            return (false, error?.GetValueOrDefault("Status") ?? "Erro ao realizar empréstimo");
        }

        public async Task<List<LoanDto>?> GetUserLoansAsync(int userId)
        {
            try { return await _httpClient.GetFromJsonAsync<List<LoanDto>>($"http://localhost:5000/loans/user/{userId}"); }
            catch { return null; }
        }

        public async Task<List<LoanDto>?> GetActiveLoansAsync()
        {
            try { return await _httpClient.GetFromJsonAsync<List<LoanDto>>("http://localhost:5000/loans/active"); }
            catch { return null; }
        }

        public async Task<bool> ReturnLoanAsync(int loanId)
        {
            var response = await _httpClient.PutAsync($"http://localhost:5000/loans/{loanId}", null);
            return response.IsSuccessStatusCode;
        }
    }

    public class LoanDto
    {
        public int id { get; set; }
        public int usuario_id { get; set; }
        public int livro_id { get; set; }
        public string status { get; set; } = string.Empty;
        public string? data_emprestimo { get; set; }
        public string? data_devolucao { get; set; }
    }
}