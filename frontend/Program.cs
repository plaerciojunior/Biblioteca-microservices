using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using BibliotecaMicroservice;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri(builder.HostEnvironment.BaseAddress) });
builder.Services.AddScoped<BibliotecaMicroservice.Handlers.UserHandler>();
builder.Services.AddScoped<BibliotecaMicroservice.Handlers.BookHandler>();
builder.Services.AddScoped<BibliotecaMicroservice.Handlers.LoanHandler>();
builder.Services.AddScoped<BibliotecaMicroservice.Handlers.AnalyticsHandler>();
builder.Services.AddScoped<BibliotecaMicroservice.Handlers.PaymentHandler>();
builder.Services.AddScoped<BibliotecaMicroservice.Services.SearchService>();
builder.Services.AddScoped<BibliotecaMicroservice.Services.AuthService>();
builder.Services.AddScoped<BibliotecaMicroservice.Services.SnackbarService>();

await builder.Build().RunAsync();
