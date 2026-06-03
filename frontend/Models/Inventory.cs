namespace BibliotecaMicroservice.Models;

public class Book
{
    public int Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Author { get; set; } = string.Empty;
    public string ISBN { get; set; } = string.Empty;
    public string Publisher { get; set; } = string.Empty;
    public string CoverUrl { get; set; } = string.Empty;
    public string Category { get; set; } = string.Empty;
    public BookStatus Status { get; set; }
    public int TotalCopies { get; set; }
    public int AvailableCopies { get; set; }
    public int LoanedCopies { get; set; }
    public List<string> Genres { get; set; } = new();
    public List<Loan> ActiveLoans { get; set; } = new();
}

public class Loan
{
    public string UserName { get; set; } = string.Empty;
    public string BookTitle { get; set; } = string.Empty;
    public string BookAuthor { get; set; } = string.Empty;
    public string CoverUrl { get; set; } = string.Empty;
    public LoanType Type { get; set; }
    public DateTime LoanDate { get; set; }
    public DateTime DueDate { get; set; }
    public DateTime? ReturnedDate { get; set; }
    public bool IsOverdue { get; set; }
}

public enum LoanType
{
    Physical,
    Online
}

public enum BookStatus
{
    Available,
    Loaned,
    Overdue
}

public class ReaderUser
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string AvatarUrl { get; set; } = string.Empty;
    public string Initials { get; set; } = string.Empty;
    public bool IsActive { get; set; }
    public DateTime JoinedDate { get; set; }
    public int BooksRead { get; set; }
    public List<Loan> ActiveLoans { get; set; } = new();
}