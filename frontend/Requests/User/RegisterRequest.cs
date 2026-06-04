using System.Text.Json.Serialization;

namespace BibliotecaMicroservice.Requests.User
{
    public class RegisterRequest
    {
        [JsonPropertyName("nome")]
        public string FullName { get; set; } = string.Empty;

        [JsonPropertyName("email")]
        public string Email { get; set; } = string.Empty;

        [JsonPropertyName("senha")]
        public string Password { get; set; } = string.Empty;

        [JsonPropertyName("tipo")]
        public string Tipo { get; set; } = "usuario";
    }
}