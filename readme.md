# Controle de Treinamentos


O projeto Controle de Treinamentos é uma aplicação web desenvolvida em Django para auxiliar na gestão de treinamentos corporativos. A plataforma permite organizar empresas, departamentos, cargos, funcionários e tipos de treinamento em um único ambiente, além de registrar a realização dos treinamentos, anexar documentos e gerar relatórios em PDF.

A aplicação foi pensada para oferecer uma visão mais prática e centralizada da rotina de gestão de capacitação, facilitando o acompanhamento de colaboradores, treinamentos exigidos por função e evidências documentais relacionadas ao processo.

## Tecnologias e stack utilizadas

O projeto utiliza as seguintes tecnologias:

- Python
- Django
- SQLite como banco de dados local
- HTML, CSS e templates Django para interface
- WeasyPrint para geração de PDF
- Pillow para manipulação de arquivos
- django-multiselectfield para controle de permissões múltiplas

## Estrutura do projeto

A estrutura principal do projeto é organizada em apps Django, cada um com responsabilidade específica:

- core: configuração geral do projeto Django, URLs principais e settings.
- company: gestão das empresas cadastradas.
- employee: gestão de departamentos, cargos e funcionários.
- training: gestão de tipos de treinamento, registros, documentos e geração de PDF.
- user: autenticação, usuários e permissões.
- decorator: lógica reutilizável para validação de permissões.
- base_templates e static: templates base e arquivos estáticos da interface.

## Licença

Este projeto é distribuído sob os termos da **GNU Affero General Public License (AGPL), versão 3 ou posterior**.

**Copyright (C) 2026 Kauãn Monteiro Silva.**

Consulte o arquivo [`LICENSE`](LICENSE) para obter o texto completo da licença.

Em resumo, você pode usar, estudar, modificar e redistribuir este software de acordo com os termos da **AGPL-3.0 ou posterior**.
