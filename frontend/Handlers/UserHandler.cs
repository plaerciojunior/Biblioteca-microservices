using System.Net.Http.Json;
using System.Threading.Tasks;
using BibliotecaMicroservice.Models;
using BibliotecaMicroservice.Requests.User;

namespace BibliotecaMicroservice.Handlers
{
    public class UserHandler
    {
        private readonly HttpClient _httpClient;

        public UserHandler(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<UserModel?> LoginAsync(LoginRequest request)
        {
            // O frontend faz a requisição para o API Gateway
            var response = await _httpClient.PostAsJsonAsync("http://localhost:5000/users/login", request);
            
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadFromJsonAsync<UserModel>();
            }
            
            return null;
        }

        public async Task<bool> LogoutAsync()
        {
            // Informa ao API Gateway/Backend sobre o logout
            var response = await _httpClient.PostAsync("http://localhost:5000/users/logout", null);
            
            // OBSERVAÇÃO IMPORTANTE:
            // O verdadeiro logout acontece limpando o armazenamento local do navegador!
            // Na UI (ou num AuthenticationStateProvider), você deve chamar algo como:
            // await _localStorage.RemoveItemAsync("jwt_token");
            return response.IsSuccessStatusCode;
        }

        public async Task<bool> RegisterAsync(RegisterRequest request)
        {
            var response = await _httpClient.PostAsJsonAsync("http://localhost:5000/users", request);
            return response.IsSuccessStatusCode;
        }
    }
}