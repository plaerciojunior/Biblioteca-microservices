using System.Net.Http.Json;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Net.Http;

namespace BibliotecaMicroservice.Handlers
{
    public class BookHandler
    {
        private readonly HttpClient _httpClient;

        public BookHandler(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<BookDto?> GetBookAsync(int id)
        {
            try
            {
                return await _httpClient.GetFromJsonAsync<BookDto>($"http://localhost:5000/books/{id}");
            }
            catch
            {
                return null;
            }
        }

        public async Task<List<BookDto>?> GetBooksAsync()
        {
            try
            {
                return await _httpClient.GetFromJsonAsync<List<BookDto>>("http://localhost:5000/books");
            }
            catch
            {
                return null;
            }
        }

        public async Task<BookDto?> CreateBookAsync(BookDto book)
        {
            var response = await _httpClient.PostAsJsonAsync("http://localhost:5000/books", book);
            if (response.IsSuccessStatusCode) return await response.Content.ReadFromJsonAsync<BookDto>();
            return null;
        }

        public async Task<BookDto?> UpdateBookAsync(int id, BookDto book)
        {
            var response = await _httpClient.PutAsJsonAsync($"http://localhost:5000/books/{id}", book);
            if (response.IsSuccessStatusCode) return await response.Content.ReadFromJsonAsync<BookDto>();
            return null;
        }

        public async Task<bool> DeleteBookAsync(int id)
        {
            var response = await _httpClient.DeleteAsync($"http://localhost:5000/books/{id}");
            return response.IsSuccessStatusCode;
        }

        public async Task<bool> UploadPdfAsync(int id, MultipartFormDataContent content)
        {
            var response = await _httpClient.PostAsync($"http://localhost:5000/books/{id}/pdf", content);
            return response.IsSuccessStatusCode;
        }
    }

    public class BookDto
    {
        public int id { get; set; }
        public string nome { get; set; } = string.Empty;
        public string autor { get; set; } = string.Empty;
        public string categoria { get; set; } = string.Empty;
        public int ano_publicacao { get; set; }
        public bool disponivel { get; set; }
        public string? pdf_url { get; set; }
    }
}