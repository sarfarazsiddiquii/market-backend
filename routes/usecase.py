from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from crewai import Crew, Process
from utils.tasks import (
    get_market_analysis_task,
    get_ai_use_cases_task,
    get_resource_collection_task,
)
from utils.agents import (
    market_research_analyst,
    ai_solutions_strategist,
    resource_collector,
)

usecase_bp = Blueprint("usecase", __name__)

@usecase_bp.route("/usecasegenerate", methods=["POST"])
@jwt_required()
def usecase_generate():
    data = request.json 
    company_name = data.get("company_name")
    
    if not company_name:
        return jsonify({"error": "Company name is required"}), 400

    try:
        market_analysis_task = get_market_analysis_task(company_name)
        analysis_crew = Crew(
            agents=[market_research_analyst],
            tasks=[market_analysis_task],
            process=Process.sequential,
        )
        market_analysis_result = analysis_crew.kickoff()
        market_analysis_raw = market_analysis_result.raw if hasattr(market_analysis_result, 'raw') else "No market analysis found"

        ai_use_cases_task = get_ai_use_cases_task(market_analysis_raw)
        ai_use_cases_crew = Crew(
            agents=[ai_solutions_strategist],
            tasks=[ai_use_cases_task],
            process=Process.sequential,
        )
        ai_use_cases_result = ai_use_cases_crew.kickoff()
        ai_use_cases_raw = ai_use_cases_result.raw if hasattr(ai_use_cases_result, 'raw') else "No AI use cases found"
        
        resource_task = get_resource_collection_task(ai_use_cases_raw)
        resource_crew = Crew(
            agents=[resource_collector],
            tasks=[resource_task],
            process=Process.sequential,
        )
        resource_result = resource_crew.kickoff()
        resource_raw = resource_result.raw if hasattr(resource_result, 'raw') else "No resources found"

        return jsonify({
            "company_name": company_name,
            "market_analysis": market_analysis_raw,
            "ai_use_cases": ai_use_cases_raw,
            "resources": resource_raw
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
