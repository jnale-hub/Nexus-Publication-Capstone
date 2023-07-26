# Nexus-Publication
School Publication website that can cater articles, search for world news, and play educational games  

### Bugs that I figured out

- I use chat-gpt when I get stuck on something and it gives me this very complicated code that I just trust for some reason
    ``` 
    # Calculate the updated game statistics
    game_stats = GameResult.objects.filter(user=user).annotate(games_played=Value(F('wordle_played'), output_field=IntegerField())).values('games_played', 'wordle_won').first()
    games_played = game_stats['games_played']
    games_won = game_stats['wordle_won']
    ```
    and then I just realized that I don't need this very weird code, I just need to make it very simple
    ```
    # Get the updated game statistics
    game_result = GameResult.objects.get(user=user)

    games_played = game_result.wordle_played
    games_won = game_result.wordle_won
    ```
    maybe because I was struggling to connect the GameResult model to the User model from the nexus_pub app. Lesson learned: when you feel really stressed in a code, maybe just get away from the screen for 5 minutes and just think.

- I was frustrated that I can't update the content of 
    ```
    // Update the DOM elements with the new statistics
    const playedElement = document.querySelector("#games-played");
    ```

    it keeps giving me null value, and then after half an hour, ~~i just realized that the whole stats's display is none.~~ console.log() really help me debugging this. Edit: That's wrong, even if the style is none, querySelector does get it still, the main problem was the name of the variable (maybe I used it too much, dunno), I tried everything I even changed the variable name to #buday and then I get it, I changed the ids and voila, it works now.

    ```const playedElement = document.querySelector("#played-num");```

- 
