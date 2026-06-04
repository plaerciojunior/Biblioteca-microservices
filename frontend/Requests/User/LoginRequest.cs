using System.Text.Json.Serialization;

namespace BibliotecaMicroservice.Requests.User
{
    public class LoginRequest
    {
        [JsonPropertyName("email")]
        public string Email { get; set; } = string.Empty;

        [JsonPropertyName("senha")]
        public string Password { get; set; } = string.Empty;
    }
}