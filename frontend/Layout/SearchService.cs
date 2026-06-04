using System;

namespace BibliotecaMicroservice.Services
{
    public class SearchService
    {
        public string SearchTerm { get; private set; } = string.Empty;
        public event Action? OnSearchChanged;

        public void SetSearchTerm(string term)
        {
            SearchTerm = term;
            OnSearchChanged?.Invoke();
        }
    }
}