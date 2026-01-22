import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import print as rprint
from mindvault_core import MindVaultCore

console = Console()

def seed_data(system: MindVaultCore):
    """Populate Qdrant with some dummy data for the demo."""
    data = [
        ("I feel overwhelmed by my workload and deadlines.", "Pomodoro Technique: Work for 25 mins, break for 5.", "Stress", 0.9),
        ("I feel very lonely and isolated in this new city.", "Join a local hobby club or meetup group.", "Loneliness", 0.8),
        ("I can't sleep because my mind is racing with thoughts.", "4-7-8 Breathing Method: Inhale 4s, Hold 7s, Exhale 8s.", "Anxiety", 0.85),
        ("I felt a sudden panic attack during the meeting.", "5-4-3-2-1 Grounding Technique.", "Panic", 0.95),
        ("I don't have energy to do anything today.", "Micro-goals: Do just one small task for 5 minutes.", "Low Mood", 0.7),
        ("I am angry at my friend for what they said.", "Write a letter expressing feelings, then burn it (don't send).", "Anger", 0.6),
    ]

    with console.status("[bold green]Seeding Memory Vault..."):
        for exp, strat, emo, score in data:
            system.add_experience(exp, strat, emo, score)
    
    console.print("[green]✓ seeded test memories into Qdrant.[/green]")

def add_memory_mode(system: MindVaultCore):
    """Allow user to manually add a new memory."""
    rprint("\n[bold magenta]--- Add New Memory ---[/bold magenta]")
    
    experience = Prompt.ask("Describe the experience/situation")
    strategy = Prompt.ask("What strategy was used?")
    emotion = Prompt.ask("What was the dominant emotion?", default="Neutral")
    score_input = Prompt.ask("Initial Effectiveness Score (0-10)", choices=[str(i) for i in range(11)], default="5")
    score = int(score_input) / 10.0

    with console.status("[bold green]Saving to Memory Vault..."):
        mem_id = system.add_experience(experience, strategy, emotion, score)
    
    rprint(f"[green]✓ Memory saved successfully! ID: {mem_id}[/green]")

def search_mode(system: MindVaultCore):
    """Existing search and recommendation flow."""
    rprint("\n[bold cyan]How are you feeling right now?[/bold cyan]")
    user_input = Prompt.ask("> ")
    
    # 1. Search & Recommend
    with console.status("[bold blue]Retrieving similar past cases..."):
        recommendations = system.find_recommendation(user_input)

    if not recommendations:
        rprint("[yellow]No similar past experiences found. Providing general strategies...[/yellow]")
        return

    # Display Top Recommendation
    top_rec = recommendations[0]
    
    rprint("\n[bold green]Recommended Strategy:[/bold green]")
    rprint(Panel(top_rec['strategy'], title="Strategy from Memory"))
    
    rprint(f"\n[dim]Based on a similar past experience:[/dim] [italic]\"{top_rec['similar_experience']}\"[/italic]")
    rprint(f"[dim]which had an Effectiveness Score of:[/dim] {top_rec['acceptance']:.2f}")

    # 2. Simulate User Choice
    if Confirm.ask("\n[bold]Do you want to try this strategy?[/bold]"):
        rprint("[green]Great! Strategy locked in.[/green]")
        
        # 3. Simulate Weekly Feedback Loop (Weeks 1-3)
        for week in range(1, 4):
            rprint(f"\n[bold yellow]--- SIMULATION: Week {week} Feedback ---[/bold yellow]")
            feedback = Prompt.ask(f"How helpful was this strategy in Week {week}? (0-10)", choices=[str(i) for i in range(11)])
            
            new_score = int(feedback) / 10.0
            
            with console.status(f"[bold magenta]Updating Memory Vault (Week {week})..."):
                system.update_feedback(
                    memory_id=top_rec['id'],
                    new_score=new_score
                )
            rprint(f"[blue]✓ Memory updated: Week {week} score = {new_score}[/blue]")
    
    else:
        rprint("[yellow]Okay, let's look for something else next time.[/yellow]")

def interactive_mode(system: MindVaultCore):
    console.clear()
    console.print(Panel.fit("[bold magenta]MindVault[/bold magenta]\n[dim]Qdrant-Powered Therapeutic Memory System[/dim]", subtitle="v1.0"))

    while True:
        rprint("\n[bold]Main Menu:[/bold]")
        rprint("1. [cyan]Find Help (Search)[/cyan]")
        rprint("2. [magenta]Add New Memory[/magenta]")
        rprint("3. [red]Exit[/red]")
        
        choice = Prompt.ask("Select an option", choices=["1", "2", "3"], default="1")

        if choice == "1":
            search_mode(system)
        elif choice == "2":
            add_memory_mode(system)
        elif choice == "3":
            rprint("[bold]Goodbye![/bold]")
            break

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Usage: python main.py [--seed]")
        return

    system = MindVaultCore()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--seed":
        seed_data(system)
    
    interactive_mode(system)

if __name__ == "__main__":
    main()
