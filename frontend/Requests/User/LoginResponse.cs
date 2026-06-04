using System.Text.Json.Serialization;
using BibliotecaMicroservice.Models;

namespace BibliotecaMicroservice.Requests.User
{
    public class LoginResponse
    {
        [JsonPropertyName("token")]
        public string Token { get; set; } = string.Empty;

        [JsonPropertyName("user")]
        public UserModel User { get; set; } = new UserModel();
    }
}