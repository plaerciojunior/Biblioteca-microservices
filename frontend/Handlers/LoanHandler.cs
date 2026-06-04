using System.Net.Http.Json;
using System.Threading.Tasks;
using System.Collections.Generic;
using System;

namespace BibliotecaMicroservice.Handlers
{
    public class LoanHandler
    {
        private readonly HttpClient _httpClient;

        public event Action? OnLoansChanged;
        public void NotifyLoansChanged() => OnLoansChanged?.Invoke();

        public LoanHandler(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<(bool Success, string Message)> CreateLoanAsync(int userId, int bookId)
        {
            var request = new { usuario_id = userId, livro_id = bookId };
            var response = await _httpClient.PostAsJsonAsync("http://localhost:5000/loans", request);
            
            if (response.IsSuccessStatusCode)
            {
                NotifyLoansChanged();
                return (true, "Empréstimo realizado");
            }
                
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

        public async Task<(bool Success, string Message)> ReturnLoanAsync(int loanId)
        {
            var response = await _httpClient.PutAsync($"http://localhost:5000/loans/{loanId}", null);
            if (response.IsSuccessStatusCode)
            {
                NotifyLoansChanged();
                return (true, "Livro devolvido com sucesso!");
            }
            
            try 
            {
                var error = await response.Content.ReadFromJsonAsync<Dictionary<string, string>>();
                return (false, error?.GetValueOrDefault("Status") ?? "Erro ao devolver livro.");
            }
            catch
            {
                return (false, "Erro interno no servidor de empréstimos.");
            }
        }

        public async Task<(bool Success, string Message)> RenewLoanAsync(int loanId)
        {
            var response = await _httpClient.PutAsync($"http://localhost:5000/loans/{loanId}/renew", null);
            if (response.IsSuccessStatusCode)
            {
                NotifyLoansChanged();
                return (true, "Livro renovado com sucesso!");
            }
            
            try
            {
                var error = await response.Content.ReadFromJsonAsync<Dictionary<string, string>>();
                return (false, error?.GetValueOrDefault("Status") ?? "Erro ao renovar livro.");
            }
            catch
            {
                return (false, "Erro interno no servidor de empréstimos.");
            }
        }

        public async Task<bool> ClearUserFinesAsync(int userId)
        {
            var response = await _httpClient.PutAsync($"http://localhost:5000/loans/user/{userId}/clear_fines", null);
            if (response.IsSuccessStatusCode)
            {
                NotifyLoansChanged();
                return true;
            }
            return false;
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