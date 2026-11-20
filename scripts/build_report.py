import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess

from docx import Document
from docx.enum.text import WD_BREAK
from docx.shared import Inches
from docx.text.paragraph import Paragraph
from lxml import etree
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
summary = pd.read_csv(OUT / "llm_runs/evaluation_summary.csv").fillna("")
runs = {name: json.loads((OUT / "llm_runs" / f"{name}.json").read_text()) for name in summary.scenario}
original = runs["original"]
missing = original["observations"]["missing"]
audit = json.loads((OUT / "explanation_audit.json").read_text())
sections = [
    ("Overview",
     "This resubmission replaces the rejected deterministic controller with an "
     "actual LLM-directed agent built using LangGraph, LangChain and MiniMax-M3. "
     "It reviews one registered public Palmer Penguins CSV and explains evidence "
     "to a person. The model interprets natural-language instructions, selects "
     "tools and decides what to do after each observation. Python enforces "
     "capability boundaries but does not prescribe the analysis sequence. "
     "The contribution is a bounded demonstration of model-directed review, "
     "not autonomous data cleaning, production readiness or scientific certification."),
    ("System Architecture and Design",
     "The persona is a cautious data-quality reviewer: inspect, explain and "
     "leave changes to a human. One agent is sufficient because the task uses "
     "a shared evidence state and no independent specialist roles. Its LangGraph "
     "StateGraph alternates llm_decision and read_only_tool nodes. LangGraph "
     "distinguishes predetermined workflows from agents whose tool use is "
     "dynamic (LangChain, n.d.). A fixed graph does not imply a fixed tool plan: "
     "the model chooses the action identity, relevance, order and final response.\n\n"
     "Six tool schemas expose load, profile, missing, duplicates, numeric and "
     "categories. LangChain's ChatOpenAI binds them to MiniMax's OpenAI-compatible "
     "endpoint (MiniMax, n.d.). Actual evaluation used MiniMax-M3; an explicitly "
     "selected OpenAI configuration exists but was not the successful provider. "
     "Keys are environment-only and absent from the submission. Optional model "
     "thinking output is disabled. Brief public action justifications and "
     "tool observations are recorded, not private chain-of-thought.\n\n"
     "Each run has fresh message history, aggregate observations, completed "
     "tools, counters, trace and a temporary DataFrame. The model receives "
     "messages; only tools access the frame. There is no persistent memory "
     "or cross-run learning. The source has 344 rows and eight columns, "
     "distributed by Horst et al. (2020) from Gorman/Palmer Station LTER data. "
     "Its CC0 attribution, original bytes and SHA-256 are included. Figure 1 "
     "shows this implemented architecture."),
    ("Decision Logic and Behavior",
     "The user supplies a natural-language instruction inside a validated "
     "Request. The LLM requests a tool with a public reason. After validation, "
     "Python executes that requested tool and returns its aggregate result "
     "as a ToolMessage. The LLM sees the accumulated history and chooses "
     "another action or finishes. This action/observation cycle is inspired "
     "by ReAct (Yao et al., 2023), not a reproduction of its tasks, prompts "
     "or reported benchmark gains.\n\n"
     "Loading must precede data checks; numeric and categories require a "
     "profile. These are tool preconditions, not a Python scheduler selecting "
     "which check comes next. Unknown tools, malformed arguments, repeated "
     "tools and violated dependencies stop safely. An early real model request "
     "contained two tools despite the single-call setting. The initial guard "
     "blocked it. The revised guard executes neither, returns rejection "
     "observations and lets the model choose one action itself. Model-turn "
     "limits also bound repeated rejections.\n\n"
     "The result wrapper independently reports full configured coverage, "
     "findings and disposition. A narrow completed task is partial_review, "
     "not a full quality certificate. Tool failures return an observation "
     "that the model can explain; further tools are unavailable after a fault. "
     "The model is not allowed to invent missing evidence or silently substitute "
     "a review when the user asks for an unsupported edit."),
    ("Safety, Reliability, and Transparency",
     "The registered source and tool names are allowlisted. Input and tool "
     "arguments are validated; source loading checks byte/shape limits, "
     "column labels and fingerprint. There are at most six tool executions "
     "and twelve model turns, including format-repair turns. The client has "
     "a sixty-second timeout setting and no automatic provider retries. "
     "These are not an end-to-end runtime or monetary guarantee. The tools "
     "cannot edit data, run shell commands or send messages; the separate "
     "evaluation harness writes the JSON/CSV artifacts.\n\n"
     "Logs preserve model-selected calls, public reasons, observations, "
     "response identifiers, usage and final answers. They are evidence of "
     "observable behavior, not faithful access to internal reasoning. "
     "Raw cell strings are not forwarded by these tools, but user instructions "
     "and aggregates reach a third-party API. Transparency, bounded authority "
     "and human accountability are risk controls consistent with NIST (2023), "
     "not certification. There is no OS isolation, general injection defense "
     "or automatic recovery from arbitrary programming errors."),
    ("Observed Behavior and Limitations",
     f"Eight current designed cases have saved real provider transcripts. "
     f"The original-data run returned {original['status']}/{original['disposition']}, "
     f"using {original['tool_calls']} tool executions and {original['model_turns']} "
     f"model turns. It found {missing['missing_cells']} missing cells across "
     f"{missing['rows_with_missing']} records, with zero full-row repeats and "
     "zero violations of the configured numeric/category rules. Missingness-only "
     f"used {' → '.join(runs['missing_only']['completed_tools'])}; duplicates-only "
     f"used {' → '.join(runs['duplicates_only']['completed_tools'])}. These distinct "
     "paths were selected from different user instructions, not Python "
     "keyword branches. The appendix records every current case.\n\n"
     f"The two-call case ended {runs['low_budget']['status']} with "
     f"{runs['low_budget']['tool_calls']} executions. The injected numeric "
     f"fault ended {runs['tool_failure']['status']}; its error observation "
     "returned to the model for an explanation. The deletion-request trace "
     "documents the actual response; no editing capability exists and the "
     "source fingerprint stayed unchanged. The reduced-column fixture is a "
     "declared projection, not discovered corruption or proof of repeated animals.\n\n"
     "The 333-row complete-case fixture with 999,999 g still returns "
     f"{runs['absurd_positive_mass']['disposition']}. The numeric tool checks "
     "only finite, positive representations and exposes no actual mass. "
     "Adding an LLM cannot reveal information its tools never return. "
     "Early retained development responses also inferred row-level overlap "
     "and overinterpreted attribute repeats. Instructions were strengthened "
     "and final responses were inspected without editing their saved prose. "
     + audit["report_summary"] + "\n\n"
     "The current suite is small, purpose-built and used during development, "
     "not an untouched reliability benchmark. Offline tests use a scripted "
     "model and check software properties; they are separate from live LLM "
     "evidence. There is no random task sample, multi-run success estimate, "
     "baseline comparison, confidence interval or independent user study."),
    ("Interpretation for a Non-Technical Audience",
     "A language model reads the request and chooses from a small set of "
     "checking tools. After each result, it decides whether another check "
     "is needed. For the full penguin table, the tools found 19 blank entries "
     "spread across 11 records. A person receives the findings; nothing is "
     "deleted or filled in. A request just about blanks leads to fewer checks "
     "than a full review. The program stops if its allowance runs out or a "
     "checking function fails. It can still miss serious problems: a test "
     "weight of 999,999 grams passed because the available rule checked only "
     "that it was a positive number. The model's written explanation can also "
     "go beyond what the checks establish. A person must inspect the evidence "
     "before making changes."),
    ("Ethical and Responsible Use Considerations",
     "A fluent explanation can create overtrust. A completed run or "
     "configured_checks_clear does not mean the data are scientifically "
     "correct. The known mass miss and explanation errors make that boundary "
     "concrete. Structured counts remain visible beside model prose, and "
     "human review—not automatic cleaning—retains authority (NIST, 2023).\n\n"
     "Deleting missing or repeated-attribute records could distort "
     "representation. The agent cannot decide that such rows identify the "
     "same animal or should be discarded. Public animal data reduce some "
     "privacy risks but do not establish safety for private human records; "
     "provider disclosure, access, consent and retention would need review. "
     "No fairness or ecological-bias assessment was performed.\n\n"
     "Replit AI assisted with planning, implementation, debugging, testing "
     "and drafting. Edward must review, understand and personalize the work "
     "under course policy. Saved provider responses are unedited evidence; "
     "constructed fixtures are labeled. Reproducible software assertions "
     "do not establish independent authorship, production safety or a passing "
     "classroom decision."),
    ("Future Improvements",
     "First, define domain-expert measurement ranges and cross-field checks, "
     "then evaluate them on new cases rather than retroactively declaring "
     "the known miss detected. Supply evidence sufficient for row-overlap "
     "questions instead of inviting the model to infer it from marginals. "
     "Test explanation grounding with independently annotated questions and "
     "repeated runs across models; report abstention and error rates separately "
     "from tool completion. More prompts alone are not a reliability proof.\n\n"
     "A deployed version would also require process isolation, end-to-end "
     "timeouts, access controls, protected audit retention, explicit provider "
     "cost limits and human approval before any future write capability. "
     "Keep these proposed controls separate from the implemented safeguards. "
     "No production deployment, automatic repair or broader dataset competence "
     "is claimed by this resubmission."),
]

references = [
    ("Horst, A. M., Hill, A. P., & Gorman, K. B. (2020). palmerpenguins: Palmer "
     "Archipelago (Antarctica) penguin data [Data set]. https://doi.org/10.5281/zenodo.3960218",
     "palmerpenguins: Palmer Archipelago (Antarctica) penguin data"),
    ("LangChain. (n.d.). Workflows and agents. https://docs.langchain.com/oss/python/langgraph/workflows-agents",
     "Workflows and agents"),
    ("MiniMax. (n.d.). OpenAI API compatibility. https://platform.minimax.io/docs/api-reference/text-openai-api",
     "OpenAI API compatibility"),
    ("National Institute of Standards and Technology. (2023). Artificial intelligence "
     "risk management framework (AI RMF 1.0). https://doi.org/10.6028/NIST.AI.100-1",
     "Artificial intelligence risk management framework (AI RMF 1.0)"),
    ("Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). "
     "ReAct: Synergizing reasoning and acting in language models. International Conference "
     "on Learning Representations. https://openreview.net/forum?id=WE_vluYUL-X",
     "International Conference on Learning Representations"),
]

parser = argparse.ArgumentParser()
parser.add_argument("template", type=Path)
args = parser.parse_args()
doc = Document(args.template)
patterns = [deepcopy(p._p) for p in doc.paragraphs]
original_styles = doc.styles.element.xml
original_section = etree.tostring(doc.sections[0]._sectPr, method="c14n", exclusive=True)
header_footer = {str(p.partname): p.blob for p in doc.part.package.parts
                 if "header" in p.content_type or "footer" in p.content_type}
body = doc._element.body
for child in list(body):
    if child is not doc.sections[0]._sectPr:
        body.remove(child)


def append_pattern(index, text=""):
    element = deepcopy(patterns[index])
    original = Paragraph(element, doc._body)
    properties = deepcopy(original.runs[0]._r.rPr) if original.runs else None
    for child in list(element):
        if child is not element.pPr:
            element.remove(child)
    body.insert(len(body) - 1, element)
    paragraph = Paragraph(element, doc._body)
    run = paragraph.add_run(text)
    if properties is not None:
        run._r.insert(0, properties)
    return paragraph


def page_break():
    append_pattern(13).runs[0].add_break(WD_BREAK.PAGE)


cover = {4: "An LLM-Directed Data-Quality Review Agent",
         6: "AI Foundations (Edward Hickman)", 7: "Udacity",
         8: "Project 6 — Agentic AI Systems: Resubmission", 9: "", 10: ""}
for index in range(11):
    append_pattern(index, cover.get(index, ""))
page_break()
append_pattern(14, cover[4])
text = f"# {cover[4]}\n\n{cover[6]}\n\n"
for heading, content in sections:
    append_pattern(19, heading)
    for paragraph in content.split("\n\n"):
        append_pattern(15, paragraph)
    text += f"## {heading}\n\n{content}\n\n"

page_break()
append_pattern(19, "Figure 1")
append_pattern(1).runs[0].add_picture(str(OUT / "architecture_diagram.png"), width=Inches(6.5))
append_pattern(15, "Note. Implemented architecture: a fixed LangGraph loop with "
               "model-selected analysis actions. The guard can reject a batch and "
               "return feedback without selecting a replacement tool. A final "
               "model explanation is paired with independently computed coverage. "
               "Invalid requests terminate before model use; local frames are not sent.")

page_break()
append_pattern(19, "Live Evaluation Record")
append_pattern(15, "Actual final-run statuses; not a success-rate estimate. "
               "Fixtures and injected faults are declared in the JSON context. "
               "See outputs/llm_runs for complete unedited transcripts.")
for row in summary.itertuples():
    append_pattern(15, f"{row.scenario}: {row.status}; {row.disposition}; "
                   f"{row.tool_calls} tool executions, {row.model_turns} model turns. "
                   f"Completed tools: {row.selected_tools or '(none)'}.")

page_break()
append_pattern(37, "References")
text += "## References\n\n"
for reference, italic_span in references:
    p = append_pattern(38)
    props = deepcopy(p.runs[0]._r.rPr)
    for run in list(p.runs):
        p._p.remove(run._r)
    before, after = reference.split(italic_span, 1)
    for value, italic in [(before, False), (italic_span, True), (after, False)]:
        run = p.add_run(value)
        if props is not None:
            run._r.insert(0, deepcopy(props))
        run.italic = italic
    text += f"{reference}\n\n"
doc.core_properties.title = cover[4]
doc.core_properties.author = cover[6]
doc.core_properties.subject = cover[8]
doc.core_properties.comments = "AI assistance disclosed. Instructor and due date not supplied."
assert doc.styles.element.xml == original_styles
assert etree.tostring(doc.sections[0]._sectPr, method="c14n", exclusive=True) == original_section
assert header_footer == {str(p.partname): p.blob for p in doc.part.package.parts
                         if "header" in p.content_type or "footer" in p.content_type}
doc.save(ROOT / "module_summary.docx")
(ROOT / "module_summary.md").write_text(text.rstrip() + "\n")
subprocess.run(["libreoffice", "-env:UserInstallation=file:///tmp/agentic-report-office",
                "--headless", "--convert-to", "pdf", "--outdir", str(ROOT),
                str(ROOT / "module_summary.docx")], check=True)
(OUT / "report_template_audit.json").write_text(json.dumps({
    "template_url": "https://docs.google.com/document/d/1cv_MjQVKnGc9sbaYiOUna2155jMEvUxACwyDax-XYWI/edit",
    "template_sha256": hashlib.sha256(args.template.read_bytes()).hexdigest(),
    "styles_preserved": True, "section_preserved": True, "headers_preserved": True,
    "omitted_fields": ["Instructor", "Due date"],
    "pdf_font": "Liberation Sans substitutes for retained Arial DOCX styles",
}, indent=2) + "\n")
