import argparse
import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent))
from agents import JobMatchAgent


def main():
    parser = argparse.ArgumentParser(
        description="JobMatch AI - Agent-based job matching",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use PDF profile
  python src/run_agent.py --pdf data/linkedin_profile.pdf
  
  # Use JSON profile  
  python src/run_agent.py --json data/linkedin_profile.json
  
  # Custom search query
  python src/run_agent.py --pdf data/resume.pdf --query "Machine Learning Engineer" --location "London"
  
  # More matches
  python src/run_agent.py --pdf data/resume.pdf --top 5
        """
    )
    
    # Profile input
    profile_group = parser.add_mutually_exclusive_group(required=False)
    profile_group.add_argument('--pdf', type=str, help='Path to PDF profile')
    profile_group.add_argument('--json', type=str, help='Path to JSON profile')
    
    # Job search parameters
    parser.add_argument('--query', type=str, default='AI engineer', 
                       help='Job search query (default: AI engineer)')
    parser.add_argument('--location', type=str, default='Berlin',
                       help='Job location (default: Berlin)')
    parser.add_argument('--top', type=int, default=3,
                       help='Number of top matches (default: 3)')
    
    # Filtering options
    parser.add_argument('--countries', nargs='+', default=['de', 'uk', 'nl'],
                       help='Valid country codes (default: de uk nl)')
    parser.add_argument('--keywords', nargs='+',
                       help='Keywords for filtering (optional)')
    
    args = parser.parse_args()
    
    # Initialize agent
    print("🤖 Initializing JobMatch AI Agent...")
    agent = JobMatchAgent()
    
    # Determine profile source
    if args.pdf:
        profile_source = "pdf"
        profile_path = args.pdf
    elif args.json:
        profile_source = "json"
        profile_path = args.json
    else:
        default_profile = Path('data/profile.pdf')
        if not default_profile.exists():
            parser.error("No profile provided and default data/profile.pdf not found")
        profile_source = "pdf"
        profile_path = str(default_profile)
    
    print(f"📋 Profile: {profile_path}")
    print(f"🔍 Query: {args.query}")
    print(f"📍 Location: {args.location}")
    print(f"🎯 Top: {args.top}")
    print("\n" + "=" * 80)
    
    # Run workflow
    results = agent.run_workflow(
        profile_source=profile_source,
        profile_path=profile_path,
        job_query=args.query,
        job_location=args.location,
        filter_countries=args.countries,
        filter_keywords=args.keywords,
        top_n=args.top
    )
    
    # Display results
    agent.display_results(results)

    if profile_source == "pdf" and isinstance(results, dict) and "profile" in results:
        output_path = Path('data/linkedin_profile.json')
        try:
            output_path.write_text(json.dumps(results["profile"], ensure_ascii=False, indent=2), encoding='utf-8')
            print(f"\n💾 Saved parsed profile to {output_path}")
        except Exception as exc:
            print(f"\n⚠️ Unable to save parsed profile: {exc}")


if __name__ == "__main__":
    main()
