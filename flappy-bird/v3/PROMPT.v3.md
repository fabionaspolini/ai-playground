# Prompt: Clone Completo do Flappy Bird (Vanilla JS + Canvas)

**Atue como um Desenvolvedor de Jogos Web Sênior especializado em HTML5 Canvas.**  
Seu objetivo é criar uma réplica completa, funcional e visualmente polida do jogo **"Flappy Bird"** utilizando exclusivamente **HTML5, CSS3 e JavaScript Puro (Vanilla JS)**. Nenhuma biblioteca externa é permitida.

---

## 1. ARQUITETURA E ESTRUTURA DO CÓDIGO

### Entrega
- **Um único arquivo** `index.html` contendo toda a estrutura HTML, CSS (na tag `<style>`) e JavaScript (na tag `<script>`).
- O arquivo deve ser **autossuficiente**: rodar apenas abrindo no navegador, sem servidor, sem dependências externas, sem arquivos de imagem.
- Todos os gráficos devem ser desenhados via Canvas API usando **formas geométricas, cores sólidas e gradientes**.

### Classes ES6 obrigatórias
Implemente as seguintes classes separadas, cada uma com responsabilidade única:

````javascript
class Bird { ... }       // Física, animação e renderização do pássaro
class Pipe { ... }       // Estado, movimento e renderização de um par de canos
class PipeManager { ... } // Geração procedural, reciclagem e scoring de canos
class Background { ... } // Camadas de fundo com paralaxe
class Game { ... }       // Game loop, estados, input, colisão e orquestração
````

### Game Loop
- Use `requestAnimationFrame` para o loop principal.
- Calcule o **delta time** (`dt`) entre frames para garantir física independente de frame rate.
- O loop deve respeitar os estados do jogo: `MENU`, `PLAYING`, `GAME_OVER`.

---

## 2. FÍSICA DO PÁSSARO

### Gravidade e impulso
- Declare uma constante `GRAVITY = 1800` (pixels/s²) aplicada a cada frame: `velocity += GRAVITY * dt`.
- Ao clicar/pressionar Espaço: aplique impulso instantâneo `velocity = -520` (pixels/s), ignorando velocidade atual.
- A velocidade vertical máxima de queda (terminal velocity) deve ser limitada a `+600` pixels/s.
- A posição Y do pássaro deve ser atualizada por: `bird.y += bird.velocity * dt`.

### Rotação visual
- O pássaro deve **rotacionar** de acordo com a velocidade vertical:
  - Subindo (velocity < 0): rotação negativa máxima de **-25 graus**.
  - Caindo (velocity > 200): rotação positiva máxima de **+90 graus** (bico apontando para baixo).
  - Interpole a rotação suavemente: `targetAngle = clamp(velocity / 10, -25, 90)`.
- A rotação deve ser aplicada com `ctx.save() / ctx.translate() / ctx.rotate() / ctx.restore()`.

### Animação de asas
- O pássaro deve ter **3 frames de animação** (asa para cima, meio, baixo) desenhados via Canvas.
- Alterne os frames a cada **120ms** durante o estado `PLAYING`.
- Durante o `GAME_OVER`, congele a animação no frame atual.

### Desenho do pássaro (sem imagens externas)
Desenhe o pássaro usando formas Canvas:
- **Corpo:** Elipse amarela/laranja com gradiente radial.
- **Asa:** Elipse menor animada (sobe e desce conforme o frame).
- **Olho:** Círculo branco + círculo preto (pupila) + pequeno reflexo branco.
- **Bico:** Dois retângulos/polígonos laranjas formando o bico aberto levemente.

---

## 3. CANOS (OBSTÁCULOS)

### Geração procedural
- Gere um novo par de canos a cada **1.5 segundos** (ajustável via constante `PIPE_INTERVAL`).
- A abertura entre cano superior e inferior deve ter **altura fixa de 160px** (constante `PIPE_GAP`).
- O centro vertical da abertura deve ser posicionado **aleatoriamente** entre `20%` e `80%` da altura do canvas.
- Canos devem iniciar fora da tela à direita (`x = canvasWidth + 10`).

### Movimento
- Todos os canos se movem para a esquerda a uma velocidade constante de **200px/s** (constante `PIPE_SPEED`).
- A velocidade pode aumentar progressivamente: a cada 5 pontos, some `+10px/s` ao `PIPE_SPEED`, até o máximo de `350px/s`.

### Reciclagem
- Quando um cano sair completamente pela esquerda da tela (`x + largura < 0`), remova-o do array (ou recicle-o).

### Desenho dos canos (sem imagens externas)
- **Corpo do cano:** Retângulo verde (`#2ECC40`) com borda mais escura (`#1a7a25`).
- **Bocal do cano:** Retângulo levemente mais largo e com cantos levemente arredondados na extremidade que aponta para o gap.
- Adicione um **gradiente lateral** (borda esquerda mais escura, centro mais claro) para dar sensação de volume.

---

## 4. CENÁRIO E FUNDO (PARALAXE)

### Camadas de fundo (da mais distante para a mais próxima)
1. **Céu:** Gradiente linear vertical do topo (`#70C5CE`) para a base (`#C9E8F0`). Estático.
2. **Nuvens:** 4 a 6 nuvens desenhadas com círculos sobrepostos (branco, opacidade 0.9). Movem-se a **30px/s** para a esquerda. Reciclar quando saírem da tela.
3. **Cidade/colinas ao fundo:** Retângulos de alturas variadas (`#8B9BB4`) simulando prédios distantes. Movem-se a **60px/s**.
4. **Chão:** Retângulo marrom/bege (`#DEB887`) na base do canvas com altura de `80px`. Move-se a **200px/s** (mesma velocidade dos canos). Adicione um padrão de "grama" (pequenos retângulos verdes) no topo do chão.

### Textura do chão animada
- O chão deve ter uma textura repetida que se move para criar a ilusão de movimento contínuo.
- Use um offset `groundOffset` que incrementa a cada frame e reinicia após completar o padrão.

---

## 5. DETECÇÃO DE COLISÃO

### Regras de colisão (Game Over é acionado quando):
1. O pássaro toca o **chão** (`bird.y + bird.radius >= canvasHeight - groundHeight`).
2. O pássaro sai pelo **topo** da tela (`bird.y - bird.radius <= 0`).
3. O hitbox do pássaro intersecta o hitbox de qualquer cano (superior ou inferior).

### Hitbox
- Use hitbox **circular** para o pássaro com raio `= 0.75 * halfHeight` (menor que o visual para ser mais justo).
- Use hitbox **retangular** para os canos (AABB).
- Implemente a função: `circleRect(cx, cy, cr, rx, ry, rw, rh)` que retorna `true` se houver interseção.

### Pós-colisão (Death Sequence)
- Ao colidir: congele os canos e o fundo (pare o movimento).
- Aplique um **flash branco** na tela (opacidade 0.6, durar 3 frames).
- O pássaro deve continuar caindo com gravidade por **0.8 segundos** antes de mostrar o modal de Game Over.

---

## 6. PONTUAÇÃO

### Regras
- O jogador marca **+1 ponto** cada vez que o pássaro passar pelo eixo X central de um par de canos (detecção de crossing: quando `pipe.x + pipe.width < bird.x` pela primeira vez).
- Use uma flag `pipe.scored = false` inicializada em cada cano; marque `true` quando o ponto for contado.

### Exibição durante o jogo
- Exiba a pontuação atual no **centro-superior do canvas** (`y = 60px`).
- Fonte: `bold 48px` com contorno preto de 3px (`ctx.strokeText`) e preenchimento branco.

### High Score
- Armazene o recorde em `localStorage` com a chave `'flappyHighScore'`.
- Leia ao iniciar: `highScore = parseInt(localStorage.getItem('flappyHighScore')) || 0`.
- Atualize se `currentScore > highScore` ao Game Over.

---

## 7. ESTADOS DO JOGO E INTERFACES (UI)

### Estado 1: MENU (Tela inicial)
- Exibir sobre o canvas (elemento HTML sobreposto ou desenhado no canvas):
  - Título **"FLAPPY BIRD"** em fonte grande e estilizada.
  - O pássaro deve estar visível flutuando levemente (animação de bob: `y += Math.sin(Date.now()/400) * 0.5`).
  - Texto piscante: **"Clique ou pressione ESPAÇO para iniciar"** (piscar a cada 600ms com `setInterval`).
  - Se existir High Score salvo, exibi-lo abaixo do título.
- Ao clicar ou pressionar Espaço: transicionar para o estado `PLAYING`.

### Estado 2: PLAYING (Jogo em andamento)
- Exibir no canvas:
  - Pontuação atual (centro-superior).
  - O jogo está ativo, física e colisão habilitadas.
- Sem overlays HTML visíveis.

### Estado 3: GAME_OVER (Fim de jogo)
Exibir um **modal HTML/CSS** sobreposto ao canvas com:
- **Fundo:** `div` semitransparente com `background: rgba(0,0,0,0.5)`, centralizado via flexbox.
- **Card central** (branco, bordas arredondadas `16px`, sombra `box-shadow`):
  - Título: **"GAME OVER"** em vermelho, fonte grande.
  - Linha com ícone de medalha + **"SCORE: [pontuação atual]"**.
  - Linha com ícone de troféu + **"BEST: [recorde]"**.
  - Se o jogador bateu o recorde, exibir badge **"NOVO RECORDE! 🏆"** em destaque.
  - Botão **"JOGAR NOVAMENTE"** estilizado (verde, hover escurece, `border-radius: 8px`, `padding: 12px 32px`).
- Ao clicar em "JOGAR NOVAMENTE": resetar todo o estado do jogo e voltar ao estado `MENU` ou diretamente para `PLAYING`.

---

## 8. RESPONSIVIDADE

- O canvas deve preencher a janela do navegador respeitando um **aspect ratio de 9:16** (portrait), centralizado horizontalmente.
- Em telas largas, o canvas fica centralizado com fundo preto nas laterais.
- Em telas pequenas (mobile), o canvas ocupa 100% da largura disponível.
- Ao redimensionar a janela (`window.addEventListener('resize', ...)`), recalcule as dimensões do canvas e reescale as posições dos elementos proporcionalmente.
- A largura de referência é **`360px`** e a altura de referência é **`640px`**. Use um fator de escala `scale = canvasWidth / 360` para todos os tamanhos e velocidades.

---

## 9. CONTROLES

| Ação | Dispositivo |
|---|---|
| Fazer o pássaro voar | Clique do mouse no canvas |
| Fazer o pássaro voar | Toque na tela (touch) |
| Fazer o pássaro voar | Tecla `Espaço` |
| Fazer o pássaro voar | Tecla `ArrowUp` |
| Iniciar/Reiniciar | Tecla `Enter` (na tela de Game Over) |

- O input deve ser bloqueado durante a **Death Sequence** (0.8 segundos pós-colisão).
- No mobile, prevenir o comportamento padrão de scroll com `event.preventDefault()` no touchstart.

---

## 10. SOM (OPCIONAL MAS RECOMENDADO)

Se implementar áudio, use a **Web Audio API** (sem arquivos externos):
- **Flap:** Tom curto ascendente (`oscillator`, frequência 600→900Hz, duração 80ms).
- **Score:** Tom ascendente duplo (dois beeps rápidos, 700Hz e 900Hz).
- **Hit:** Ruído curto descendente (frequência 400→100Hz, duração 200ms).
- Todos os sons devem ser gerados programaticamente com `AudioContext`.

---

## 11. CONSTANTES CONFIGURÁVEIS

Defina todas as constantes no topo do script, agrupadas e comentadas:

````javascript
// --- FÍSICA ---
const GRAVITY         = 1800;  // px/s²
const FLAP_FORCE      = -520;  // px/s (impulso para cima)
const TERMINAL_VEL    = 600;   // px/s (velocidade máxima de queda)

// --- CANOS ---
const PIPE_GAP        = 160;   // px (abertura entre canos)
const PIPE_WIDTH      = 60;    // px
const PIPE_SPEED_BASE = 200;   // px/s
const PIPE_SPEED_MAX  = 350;   // px/s
const PIPE_INTERVAL   = 1500;  // ms entre novos canos

// --- PÁSSARO ---
const BIRD_RADIUS     = 18;    // px (raio visual)
const BIRD_HITBOX_R   = 14;    // px (raio do hitbox)
const ANIM_INTERVAL   = 120;   // ms entre frames de asa

// --- CANVAS ---
const BASE_WIDTH      = 360;   // px (largura de referência)
const BASE_HEIGHT     = 640;   // px (altura de referência)
const GROUND_HEIGHT   = 80;    // px
````

---

## 12. CRITÉRIOS DE QUALIDADE DO CÓDIGO

- **Zero variáveis globais** fora das classes e constantes declaradas.
- **Comentários** em cada método explicando sua responsabilidade (em português ou inglês).
- **Sem memory leaks:** cancelar `requestAnimationFrame` e limpar `setInterval` ao entrar em Game Over.
- **Funções utilitárias** separadas: `clamp(val, min, max)`, `circleRect(...)`, `randomBetween(min, max)`.
- O código deve passar sem erros no console do navegador.
- Evite código duplicado: a lógica de reset do jogo deve estar em um único método `game.reset()`.

---

## RESUMO DO FLUXO COMPLETO

````
[Abrir página]
      ↓
[Estado: MENU] → Pássaro flutuando, texto piscando, high score exibido
      ↓ (clique/espaço)
[Estado: PLAYING] → Física ativa, canos gerados, paralaxe rolando, score incrementando
      ↓ (colisão detectada)
[Death Sequence] → Flash branco, canos congelam, pássaro cai por 0.8s
      ↓
[Estado: GAME_OVER] → Modal HTML exibido, score/recorde/botão reiniciar
      ↓ (botão reiniciar)
[game.reset()] → Volta ao MENU (ou diretamente ao PLAYING)
````
