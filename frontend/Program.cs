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

await builder.Build().RunAsync();
