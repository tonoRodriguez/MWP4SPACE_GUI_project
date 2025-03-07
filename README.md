Pyhton code for fast PIC component design and fast PDK design

This project starts as a compilation of all the design I am makingduring my industrial PhD. I compiles several technologies that I needed to test. The idea of this project is to have a tool that allows users that are and aren't familiar with Lumerical design fast simple componets with templates that were already proven. This will allow to
participate in MWP even if theres not much time to design.

Technologies available:

- AL2O3 for participating in the Alubia run

- LNOI_CG: PDK for participating in the LNOI run with CamGraphics: It's a rib waveguide 

```mermaid
graph TD;
    A[SiO2] -->|h_f| B[Lithium Niobate];
    B -->|h_e| C[Patrón grabado];
    
    style A fill:#f4a988,stroke:#000,stroke-width:2px;
    style B fill:#5b9bd5,stroke:#000,stroke-width:2px;
    style C fill:#ffffff,stroke:#000,stroke-width:2px;

    subgraph Etiquetas
        D(Ángulo θ)
        E(Ancho w)
    end


-