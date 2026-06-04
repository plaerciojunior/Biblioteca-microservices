using System.Net.Http.Json;
using System.Threading.Tasks;

namespace BibliotecaMicroservice.Handlers
{
    public class PaymentHandler
    {
        private readonly HttpClient _httpClient;
        public PaymentHandler(HttpClient httpClient) { _httpClient = httpClient; }

        public async Task<bool> ProcessPaymentAsync(int userId, double amount, string cardNumber)
        {
            var request = new { usuario_id = userId, valor = amount, cartao = cardNumber };
            var response = await _httpClient.PostAsJsonAsync("http://localhost:5000/payments/pay", request);
            
            return response.IsSuccessStatusCode;
        }
    }
}