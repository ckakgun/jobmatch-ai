import argparse
from pathlib import Path
import sys
import glob
sys.path.append(str(Path(__file__).parent))
from agents import JobMatchAgent


def find_pdf_files():
    """Find all PDF files in data directory"""
    data_dir = Path(__file__).parent.parent / "data"
    pdf_files = list(data_dir.glob("*.pdf"))
    return [str(f) for f in pdf_files]


def interactive_mode():
    """Interactive mode for easy job search"""
    print("\n" + "="*80)
    print("🎯 JobMatch AI - Interactive Mode")
    print("="*80)
    
    # 1. Select PDF
    pdf_files = find_pdf_files()
    if not pdf_files:
        print("\n❌ No PDF files found in data/ directory")
        print("Please add your LinkedIn profile PDF to data/")
        return
    
    print(f"\n📄 Found {len(pdf_files)} PDF file(s):")
    for i, pdf in enumerate(pdf_files, 1):
        filename = Path(pdf).name
        print(f"  {i}. {filename}")
    
    if len(pdf_files) == 1:
        selected_pdf = pdf_files[0]
        print(f"\n✓ Using: {Path(selected_pdf).name}")
    else:
        choice = input(f"\nSelect PDF (1-{len(pdf_files)}): ").strip()
        try:
            selected_pdf = pdf_files[int(choice) - 1]
        except (ValueError, IndexError):
            print("Invalid selection")
            return
    
    # 2. Job query
    print("\n🔍 Job Search Query")
    query = input("Enter job title/keywords (default: AI engineer): ").strip()
    if not query:
        query = "AI engineer"
    
    # 3. Location
    location = input("Enter location (default: Berlin): ").strip()
    if not location:
        location = "Berlin"
    
    # 4. Number of matches
    top_n = input("Number of top matches (default: 3): ").strip()
    if not top_n:
        top_n = 3
    else:
        try:
            top_n = int(top_n)
        except ValueError:
            top_n = 3
    
    # 5. Keywords (optional)
    print("\n🎯 Filtering Keywords (optional)")
    print("   Example: pytorch tensorflow nlp")
    keywords_input = input("Enter keywords (press Enter to skip): ").strip()
    keywords = keywords_input.split() if keywords_input else None
    
    # Run workflow
    print("\n" + "="*80)
    agent = JobMatchAgent()
    
    results = agent.run_workflow(
        profile_source="pdf",
        profile_path=selected_pdf,
        job_query=query,
        job_location=location,
        filter_keywords=keywords,
        top_n=top_n
    )
    
    agent.display_results(results)


def quick_start():
    """Quick start with auto-detected PDF and default settings"""
    print("\n" + "="*80)
    print("🚀 JobMatch AI - Quick Start")
    print("="*80)
    
    # Auto-detect PDF
    pdf_files = find_pdf_files()
    if not pdf_files:
        print("\n❌ No PDF files found in data/ directory")
        print("💡 Please add your LinkedIn profile PDF to data/")
        return
    
    # Use first PDF found
    selected_pdf = pdf_files[0]
    print(f"\n📄 Auto-detected: {Path(selected_pdf).name}")
    print(f"🔍 Query: AI engineer (default)")
    print(f"📍 Location: Berlin (default)")
    print(f"🎯 Top: 3 matches")
    
    proceed = input("\n▶️  Press Enter to start, or 'n' to cancel: ").strip().lower()
    if proceed == 'n':
        print("Cancelled.")
        return
    
    # Run with defaults
    print("\n" + "="*80)
    agent = JobMatchAgent()
    
    results = agent.run_workflow(
        profile_source="pdf",
        profile_path=selected_pdf,
        job_query="AI engineer",
        job_location="Berlin",
        top_n=3
    )
    
    agent.display_results(results)


def main():
    parser = argparse.ArgumentParser(
        description="JobMatch AI - Agent-based job matching",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick start (auto-detect PDF, use defaults)
  python src/run_agent.py
  
  # Interactive mode
  python src/run_agent.py --interactive
  
  # Use specific PDF
  python src/run_agent.py --pdf data/linkedin_profile.pdf
  
  # Use JSON profile  
  python src/run_agent.py --json data/linkedin_profile.json
  
  # Custom search
  python src/run_agent.py --pdf data/resume.pdf --query "ML Engineer" --location "London" --top 5
  
  # With keyword filtering
  python src/run_agent.py --pdf data/resume.pdf --keywords pytorch tensorflow nlp
        """
    )
    
    # Profile input
    profile_group = parser.add_mutually_exclusive_group(required=False)
    profile_group.add_argument('--pdf', type=str, help='Path to PDF profile')
    profile_group.add_argument('--json', type=str, help='Path to JSON profile')
    profile_group.add_argument('--interactive', '-i', action='store_true', 
                              help='Interactive mode (ask questions)')
    
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
    
    # Mode selection
    if args.interactive:
        # Interactive mode
        interactive_mode()
        return
    
    # Check if any profile specified
    if not args.pdf and not args.json:
        # Quick start mode (no arguments)
        quick_start()
        return
    
    # Standard CLI mode
    print("🤖 Initializing JobMatch AI Agent...")
    agent = JobMatchAgent()
    
    # Determine profile source
    if args.pdf:
        profile_source = "pdf"
        profile_path = args.pdf
    else:
        profile_source = "json"
        profile_path = args.json
    
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


if __name__ == "__main__":
    main()

