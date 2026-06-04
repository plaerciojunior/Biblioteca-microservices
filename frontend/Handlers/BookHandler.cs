using System.Net.Http.Json;
using System.Threading.Tasks;
using System.Collections.Generic;

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