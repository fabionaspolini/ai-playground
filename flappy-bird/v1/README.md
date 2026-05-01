
| Model                                        | Status                         |
|----------------------------------------------|--------------------------------|
| Claude Sonnet 4.6                            | Fisica e gráficos excelentes   |
| Gemini pro                                   | Física boa e gráficos medianos |
| Self hosted qwen 3.5 9b - thinking disabled  | Código não executa             |
| Self hosted qwen 3.6 27b - thinking disabled | Física boa e gráficos medianos |

## Setup

Ryzem 5600G, 32 Gb de RAM com 16 compartilhado pra VRAM.
Sem placa de vídeo dedicada.

### Statistics

**qwen 3.6 27b** → Total time: 43 min, TFT: 27s, Total token: 4647

## Claude Code CLI - NO_THINKING

Modelo: com Sonnet 4.6

**Créditos monitorados no platform.claude.com**

- Início: $ 2.38
- Fim: $ 2.24
- Gasto: $ 0.14

**Usage statistics**

Session                                                                                                                                                                              
Total cost:            $0.1423                                                                                                                                                       
Total duration (API):  1m 20s                                                                                                                                                        
Total duration (wall): 3m 32s                                                                                                                                                        
Total code changes:    505 lines added, 0 lines removed
Usage by model:                                                                                                                                                                      
claude-haiku-4-5:  894 input, 19 output, 0 cache read, 0 cache write ($0.0010)                                                                                                   
claude-sonnet-4-6:  3 input, 5.9k output, 27.4k cache read, 11.9k cache write ($0.1413) 

## Claude Code CLI - THINKING

Modelo: com Sonnet 4.6

**Créditos monitorados no platform.claude.com**

- Início: $ 1.09
- Fim: $ -0.06
- Gasto: $ 1.15

**Usage statistics**

Session                                                                                                                                                                          
Total cost:            $1.15                                                               
Total duration (API):  11m 55s                                                                                                                                                   
Total duration (wall): 14m 5s                                                                                                                                                    
Total code changes:    628 lines added, 0 lines removed
Usage by model:
claude-haiku-4-5:  894 input, 18 output, 0 cache read, 0 cache write ($0.0010)
claude-sonnet-4-6:  6 input, 63.6k output, 31.8k cache read, 50.6k cache write ($1.15)
