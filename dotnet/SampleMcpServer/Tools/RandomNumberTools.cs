using System.ComponentModel;
using ModelContextProtocol.Server;

/// <summary>
/// Sample MCP tools for demonstration purposes.
/// These tools can be invoked by MCP clients to perform various operations.
/// </summary>
internal class RandomNumberTools
{
    [McpServerTool]
    [Description("Generates a random number between the specified minimum and maximum values.")]
    public int GetRandomNumber(
        [Description("Minimum value (inclusive)")]
        int min = 0,
        [Description("Maximum value (exclusive)")]
        int max = 100)
    {
        return Random.Shared.Next(min, max);
    }

    // criar tool para consultar cep no serviço viacep.com.br
    // faltou os annotations
    [McpServerTool]
    public async Task<string> GetCepInfoAsync(string cep)
    {
        using (var client = new HttpClient())
        {
            var response = await client.GetAsync($"https://viacep.com.br/ws/{cep}/json/");
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
        }
    }


}
