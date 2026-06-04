using System;
using System.Threading.Tasks;

namespace BibliotecaMicroservice.Services
{
    public class SnackbarService
    {
        public event Action? OnChange;
        public string Message { get; private set; } = "";
        public bool IsError { get; private set; } = false;
        public bool IsVisible { get; private set; } = false;

        public void Show(string message, bool isError = false)
        {
            Message = message;
            IsError = isError;
            IsVisible = true;
            OnChange?.Invoke();

            Task.Run(async () =>
            {
                await Task.Delay(3000);
                IsVisible = false;
                OnChange?.Invoke();
            });
        }
    }
}