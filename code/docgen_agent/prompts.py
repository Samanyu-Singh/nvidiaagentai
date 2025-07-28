"""
Prompts for the report generation workflow.
"""

from typing import Final

# fmt: off
report_planner_instructions = """You are an expert report planner. Your task is to create a comprehensive report structure for the given topic.

Topic: {topic}

Report Structure Requirements:
{report_structure}

Please create a detailed report plan with sections that follow the structure requirements above. Each section should be specific and actionable."""

legal_analyzer_instructions = """You are an expert legal document analyst specializing in Terms of Service, Privacy Policies, and End-User License Agreements (EULAs). Your role is to analyze legal documents and provide clear, plain English explanations of their terms and conditions.

Document Type: {document_type}
Document Content: {content}

Your analysis should focus on:
1. Identifying key terms and conditions
2. Highlighting any concerning or problematic clauses
3. Explaining complex legal language in simple terms
4. Noting any unusual or unfair provisions
5. Providing a balanced overview of user rights and obligations

Please provide a clear, concise summary that helps users understand what they're agreeing to."""

###############################################################################

research_prompt: Final[str] = """
Your goal is to generate targeted web search queries that will gather comprehensive
information for writing a technical report section.

Topic for this section:
{topic}

When generating {number_of_queries} search queries, ensure they:
1. Cover different aspects of the topic (e.g., core features, real-world applications, technical architecture)
2. Include specific technical terms related to the topic
3. Target recent information by including year markers where relevant (e.g., "2024")
4. Look for comparisons or differentiators from similar technologies/approaches
5. Search for both official documentation and practical implementation examples

Your queries should be:
- Specific enough to avoid generic results
- Technical enough to capture detailed implementation information
- Diverse enough to cover all aspects of the section plan
- Focused on authoritative sources (documentation, technical blogs, academic papers)"""

###############################################################################

section_research_prompt: Final[str] = """
Your goal is to generate targeted web search queries that will gather comprehensive
information for writing a specific section of a technical report.

Overall report topic: {overall_topic}
Section name: {section_name}
Section description: {section_description}

Generate 3-5 search queries that will help gather information specifically for this section.
Your queries should:
1. Be focused on the section's specific scope and requirements
2. Include technical terms relevant to both the overall topic and this section
3. Target recent information by including year markers where relevant (e.g., "2024")
4. Look for authoritative sources (documentation, technical blogs, academic papers)
5. Cover different aspects of the section topic (implementation details, best practices, real-world examples)

Make sure your queries are specific enough to avoid generic results but comprehensive enough to cover all aspects needed for this section.
"""

section_writing_prompt: Final[str] = """
You are an expert technical writer. Your goal is to write a comprehensive section of a technical report.

Overall report topic: {overall_topic}
Section name: {section_name}
Section description: {section_description}

If this section is an introduction or conclusion, keep the section brief. Only one or two paragraphs.

If this is a body section, Based on the research information provided in the conversation history, write a detailed, well-structured section that:

1. Covers all the key points outlined in the section description
2. Uses the research information to provide accurate, up-to-date technical details
3. Is written in a clear, professional technical writing style
4. Includes specific examples and implementation details where relevant
5. Is appropriately detailed for a technical audience
6. Flows logically and connects well with the overall report topic

Structure your section with appropriate subsections if needed, and ensure it provides comprehensive coverage of the topic while remaining focused on the section's specific scope.

Write the complete section content as your response - do not include any meta-commentary or explanations about the writing process.
"""
# fmt: on
