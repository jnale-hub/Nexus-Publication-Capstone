
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

### Lesson Learned

- I should commit more often

    I realized that you can open two terminal, so you can commit even the server is running. I thought that it was such a hassle to always `control + c` to stop the server and to commit and run the server again, but gosh how stupid lol.

    I also learned that you can copy relevant path to easily put the file you can add, lol. I always do `git add .` when I try to commit and the whole things comes with it. I should have commit every chunk of code that I added so that I can easily track the chnges I made the whole time. Now, I commit often and I am getting better at it, I also learned that when I commit I should use imperative tone :>

- I should write more, so that I can improve my typing skills because it's fun, lol. I kinda missed writing short stories so it can be more nurishing rather than just coding and getting stressed from time to time.

- 

### Ideas and Plans 

- Update the Rankings with Javascript

    In wordle rankings, I am kind of bothered that the data in the statistics section get updated even without reloading, so it is alos  great idea that the ranking do that too, but I know it will take more effort and my javascript is not that advance to to build the best javascript code with animation in them like an arrow down or even arrow up if the place changed. 

    So one thing that I think can be an alternatve is just put a little question mark there that says 'the page needs to reload to get the latest ranking' like that.

    I also want to have 'see more' button so that it would not limit to just top 5. 

- 
