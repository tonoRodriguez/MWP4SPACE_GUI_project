Pyhton code for fast PIC component design and fast PDK design

This project starts as a compilation of all the design I am makingduring my industrial PhD. I compiles several technologies that I needed to test. The idea of this project is to have a tool that allows users that are and aren't familiar with Lumerical design fast simple componets with templates that were already proven. This will allow to
participate in MWP even if theres not much time to design.

Technologies available:

- AL2O3 for participating in the Alubia run

- LNOI_CG: PDK for participating in the LNOI run with CamGraphics: It's a rib waveguide 
```html
<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
  <!-- Fondo SiO2 -->
  <rect x="0" y="150" width="400" height="150" fill="#f4a988" />
  <text x="200" y="250" font-size="20" font-weight="bold" fill="black" text-anchor="middle">SiO₂</text>

  <!-- Capa de Lithium Niobate -->
  <rect x="0" y="50" width="400" height="100" fill="#5b9bd5" />
  <text x="200" y="110" font-size="18" font-weight="bold" fill="black" text-anchor="middle">Lithium Niobate</text>

  <!-- Patrón grabado -->
  <polygon points="150,50 180,50 200,70 220,50 250,50 250,100 150,100" fill="white" stroke="black" stroke-width="2"/>
  
  <!-- Etiquetas -->
  <text x="185" y="40" font-size="12" fill="black">θ</text>
  <line x1="180" y1="50" x2="185" y2="60" stroke="black"/>
  
  <text x="195" y="30" font-size="12" fill="black">w</text>
  <line x1="180" y1="25" x2="250" y2="25" stroke="black"/>
  <line x1="180" y1="25" x2="180" y2="50" stroke="black"/>
  <line x1="250" y1="25" x2="250" y2="50" stroke="black"/>

  <text x="260" y="70" font-size="12" fill="black">hₑ</text>
  <line x1="250" y1="50" x2="270" y2="50" stroke="black"/>
  <line x1="250" y1="100" x2="270" y2="100" stroke="black"/>
  <line x1="270" y1="50" x2="270" y2="100" stroke="black" stroke-dasharray="4"/>

  <text x="10" y="120" font-size="12" fill="black">h_f</text>
  <line x1="20" y1="50" x2="40" y2="50" stroke="black"/>
  <line x1="20" y1="150" x2="40" y2="150" stroke="black"/>
  <line x1="40" y1="50" x2="40" y2="150" stroke="black" stroke-dasharray="4"/>

  <!-- Ejes coordenados -->
  <line x1="320" y1="50" x2="320" y2="30" stroke="black"/>
  <text x="325" y="30" font-size="12" fill="black">X</text>
  <line x1="320" y1="50" x2="340" y2="50" stroke="black"/>
  <text x="345" y="55" font-size="12" fill="black">Z</text>
  <circle cx="320" cy="50" r="5" stroke="black" fill="none"/>
  <text x="305" y="70" font-size="12" fill="black">Y</text>
</svg>


-