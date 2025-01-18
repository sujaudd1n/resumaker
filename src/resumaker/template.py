template = {
    "license": r"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Medium Length Professional CV
% LaTeX Template
% Version 3.0 (December 17, 2022)
%
% This template originates from:
% https://www.LaTeXTemplates.com
%
% Author:
% Vel (vel@latextemplates.com)
%
% Original author:
% Trey Hunner (http://www.treyhunner.com/)
%
% License:
% CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%----------------------------------------------------------------------------------------
%	PACKAGES AND OTHER DOCUMENT CONFIGURATIONS
%----------------------------------------------------------------------------------------
""",
    "setup": r"""
\documentclass[
	%a4paper, % Uncomment for A4 paper size (default is US letter)
	11pt, % Default font size, can use 10pt, 11pt or 12pt
]{resume} % Use the resume class

%\usepackage{ebgaramond} % Use the EB Garamond font
\usepackage{hyperref}
\hypersetup
{
    colorlinks=true,
    urlcolor=blue
}

\input{glyphtounicode}
\pdfgentounicode=1
""",
    "contact": r"""
\name{Md Sujauddin Sekh} % Your name to appear at the top

% You can use the \address command up to 3 times for 3 different addresses or pieces of contact information
% Any new lines (\\) you use in the \address commands will be converted to symbols, so each address will appear as a single line.

\address{West Bengal, India} % Main address

% \address{123 Pleasant Lane \\ City, State 12345} % A secondary address (optional)

\address{\raisebox{-2px}{\includegraphics[width=10px]{icons/phone.png}}  +91 9932187051 \\ \raisebox{-2px}{\includegraphics[width=10px]{icons/mail.png}} sksujj@gmail.com \\ \raisebox{-2px}{\includegraphics[width=10px]{icons/linkedin.png}} \href{https://www.linkedin.com/in/sujaudd1n/}{linkedin.com/in/sujaudd1n} \\ \raisebox{-2px}{\includegraphics[width=10px]{icons/github.png}} \href{https://github.com/sujaudd1n}{github.com/sujaudd1n}} % Contact information
""",
    "main": r"""
\begin{document}
$CONTENT
\end{document}
""",
}
