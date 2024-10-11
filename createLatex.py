import json
import imgkit
import os


class CreateLatex:
    def __init__(self, ipynb_path, save_path, title, author):
        self.ipynb_path = ipynb_path
        self.save_path = save_path
        self.title = title
        self.author = author
        self.data = self.load_ipynb()
        self.latex_list = []
        self.figure_nr = 0
        self.graphics_path = "graphics/"

    def create_head(self):
        head = r"""
\documentclass[journal,onecolumn]{IEEEtran}

\usepackage{listings}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{titlesec}
\usepackage{graphicx}
\usepackage{float}
\usepackage{dblfloatfix}
\usepackage{amsmath}
\setcounter{MaxMatrixCols}{32}

\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}

\lstdefinestyle{mystyle}{
    backgroundcolor=\color{backcolour},   
    commentstyle=\color{codegreen},
    keywordstyle=\color{magenta},
    numberstyle=\tiny\color{codegray},
    stringstyle=\color{codepurple},
    basicstyle=\ttfamily\footnotesize,
    breakatwhitespace=false,         
    breaklines=true,                 
    captionpos=b,                    
    keepspaces=true,                 
    numbers=left,                    
    numbersep=5pt,                  
    showspaces=false,                
    showstringspaces=false,
    showtabs=false,                  
    tabsize=2
}

\lstset{style=mystyle}


% correct bad hyphenation here
\hyphenation{op-tical net-works semi-conduc-tor}


\begin{document}"""
        return head
    
    def create_title(self):
        title = f"""
\\title{{{self.title}}}

\\author{{{self.author}}}

\\maketitle"""
        return title
    
    def create_code_section(self, code):
        code_section = f"""
\\begin{{lstlisting}}[language=Python]
{code}
\\end{{lstlisting}}"""
        return code_section
    
    def convert_markdown(self, markdown):
        if markdown.startswith("#"):
            return f"\\section{{{markdown.replace('#', '').replace('_', '-')}}}"
        elif markdown.startswith("##"):
            return f"\\subsection{{{markdown.replace('##', '').replace('_', '-')}}}"
        else:
            return markdown.replace('_', '-')

    def load_ipynb(self):
        with open(self.ipynb_path, "r") as f:
            data = json.load(f)
        return data
    
    def create_foot(self):
        foot = r"""
%\bibliographystyle{ieeetr}
%\bibliography{refrences}
\end{document}
"""
        return foot
    
    def handle_output(self, output):
        if output["output_type"] == "stream":
            return f"""
Output:
\\begin{{lstlisting}}[language=bash]
{''.join(output['text'])}
\\end{{lstlisting}}"""
        elif output["output_type"] == "execute_result":
            if 'text/html' in output['data']:
                html = output['data']['text/html']
                self.create_figure_file(html, f"figure_{self.figure_nr}")
                self.figure_nr += 1
                return f"\\begin{{figure}}[H]\n\\centerline{{\\includegraphics[width=18.5cm]{{graphics/figure_{self.figure_nr-1}.jpg}}}}\n\\label{{figure {self.figure_nr-1}}}\n\\end{{figure}}"
            elif 'text/plain' in output['data']:
                return f"""
Output:
\\begin{{lstlisting}}[language=bash]
{''.join(output['data']['text/plain'])}
\\end{{lstlisting}}"""
        elif output["output_type"] == "display_data":
            if 'text/html' in output['data']:
                html = output['data']['text/html']
                self.create_figure_file(html, f"figure_{self.figure_nr}")
                self.figure_nr += 1
                return f"\\begin{{figure}}[H]\n\\centerline{{\\includegraphics[width=18.5cm]{{graphics/figure_{self.figure_nr-1}.jpg}}}}\n\\label{{figure {self.figure_nr-1}}}\n\\end{{figure}}"

    def create_figure_file(self, output, file_name):
        html = ''.join(output)
        os.makedirs(self.graphics_path, exist_ok=True)
        imgkit.from_string(html, f"{self.graphics_path}/{file_name}.jpg")
    
    def create_latex(self):
        last_cell_code = False
        self.latex_list.append(self.create_head())
        self.latex_list.append(self.create_title())
        for cell in self.data["cells"]:
            if cell["cell_type"] == "markdown":
                self.latex_list.append(self.convert_markdown("".join(cell["source"])))
                last_cell_code = False
            elif cell["cell_type"] == "code":
                if not last_cell_code:
                    self.latex_list.append("\n\\subsubsection{{Code}}")
                self.latex_list.append(self.create_code_section("".join(cell["source"])))
                last_cell_code = True
                for output in cell["outputs"]:
                    self.latex_list.append(self.handle_output(output))
        self.latex_list.append(self.create_foot())


    def save_latex(self):
        with open(self.save_path, "w") as f:
            f.write("\n".join(self.latex_list))
        

if __name__ == "__main__":
    ipynb_path = "example.ipynb"
    save_path = "example.tex"
    title = "Example"
    author = "Author"
    cl = CreateLatex(ipynb_path, save_path, title, author)
    cl.create_latex()
    cl.save_latex()