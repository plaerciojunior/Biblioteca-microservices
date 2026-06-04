using Microsoft.JSInterop;
using System.Text.Json;
using System.Collections.Generic;
using System;
using System.Threading.Tasks;

namespace BibliotecaMicroservice.Services
{
    public class AuthService
    {
        private readonly IJSRuntime _jsRuntime;
        public event Action? OnAuthStateChanged;
        public int? CurrentUserId { get; private set; }
        public string? CurrentUserName { get; private set; }

        public AuthService(IJSRuntime jsRuntime)
        {
            _jsRuntime = jsRuntime;
        }

        public async Task InitializeAsync()
        {
            var token = await _jsRuntime.InvokeAsync<string>("localStorage.getItem", "jwt_token");
            if (!string.IsNullOrEmpty(token))
            {
                ExtractClaims(token);
            }
        }

        public async Task LoginAsync(string token)
        {
            await _jsRuntime.InvokeVoidAsync("localStorage.setItem", "jwt_token", token);
            ExtractClaims(token);
            OnAuthStateChanged?.Invoke();
        }

        public async Task LogoutAsync()
        {
            await _jsRuntime.InvokeVoidAsync("localStorage.removeItem", "jwt_token");
            CurrentUserId = null;
            CurrentUserName = null;
            OnAuthStateChanged?.Invoke();
        }

        private void ExtractClaims(string jwt)
        {
            try
            {
                var payload = jwt.Split('.')[1];
                var jsonBytes = ParseBase64WithoutPadding(payload);
                var claims = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(jsonBytes);
                
                if (claims != null && claims.TryGetValue("id", out var idElement))
                {
                    CurrentUserId = idElement.GetInt32();
                }
                if (claims != null && claims.TryGetValue("email", out var emailElement))
                {
                    CurrentUserName = emailElement.GetString();
                }
            }
            catch
            {
                CurrentUserId = null;
                CurrentUserName = null;
            }
        }

        private byte[] ParseBase64WithoutPadding(string base64)
        {
            switch (base64.Length % 4)
            {
                case 2: base64 += "=="; break;
                case 3: base64 += "="; break;
            }
            return Convert.FromBase64String(base64);
        }
    }
}