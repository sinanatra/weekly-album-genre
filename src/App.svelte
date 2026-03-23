<script>
  import { onMount } from 'svelte';

  const DATA_URL = 'https://raw.githubusercontent.com/sinanatra/weekly-album-genre/master/data.json';

  let genres = [];
  let sorted = false;
  let activeGenre = null;

  function makeColorGenerator() {
    const golden_ratio_conjugate = 0.98;
    let h = Math.random();

    function hue2rgb(p, q, t) {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1 / 6) return p + (q - p) * 6 * t;
      if (t < 1 / 2) return q;
      if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
      return p;
    }

    function hslToRgb(h, s, l) {
      const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
      const p = 2 * l - q;
      const r = hue2rgb(p, q, h + 1 / 3);
      const g = hue2rgb(p, q, h);
      const b = hue2rgb(p, q, h - 1 / 3);
      return '#' + Math.round(r * 255).toString(16).padStart(2, '0')
               + Math.round(g * 255).toString(16).padStart(2, '0')
               + Math.round(b * 255).toString(16).padStart(2, '0');
    }

    return () => {
      h += golden_ratio_conjugate;
      h %= 1;
      return hslToRgb(h, 0.5, 0.60);
    };
  }

  onMount(async () => {
    const res = await fetch(DATA_URL);
    const data = await res.json();
    const nextColor = makeColorGenerator();

    genres = Object.entries(data)
      .map(([genre, albums]) => ({ genre, albums }))
      .sort((a, b) => b.albums.length - a.albums.length)
      .map(g => ({ ...g, color: nextColor(), width: Math.random() * 99 + '%' }));
  });

  function toggleSort() {
    if (!sorted) {
      const max = genres[0].albums.length;
      genres = genres.map(g => ({
        ...g,
        width: Math.round(g.albums.length * 99 / max) + '%',
      }));
    } else {
      genres = genres.map(g => ({
        ...g,
        width: Math.random() * 80 + '%',
      }));
    }
    sorted = !sorted;
  }

  function handleClick(genre) {
    activeGenre = activeGenre === genre ? null : genre;
  }
</script>

<div>
  <p>
    This website shows the artists I listen to most in the current week.<br>
    And <button class="sort" on:click={toggleSort}>Sorts</button> them by the most frequent genres.
  </p>
</div>

<div id="visualisation">
  {#each genres as item (item.genre)}
    <div
      class="words"
      style="width: {item.width}; background: {item.color};"
      on:click={() => handleClick(item.genre)}
      role="button"
      tabindex="0"
      on:keydown={(e) => e.key === 'Enter' && handleClick(item.genre)}
    >
      {item.genre}
      {#if activeGenre === item.genre}
        <div class="links">
          {#each item.albums as artistId}
            <iframe
              src="https://open.spotify.com/embed/artist/{artistId}"
              width="300"
              height="80"
              frameborder="0"
              allowtransparency="true"
              allow="encrypted-media"
              title={artistId}
            ></iframe>
          {/each}
        </div>
      {/if}
    </div>
  {/each}
</div>

<style>
  :global(body) {
    font-family: Arial, Helvetica, sans-serif;
    background-color: white;
    color: black;
    margin: 0;
  }

  #visualisation {
    width: 100vw;
    display: block;
  }

  p {
    font-size: 24px;
    margin: 0;
    padding: 0.5%;
  }

  .words {
    font-size: 24px;
    margin: 0;
    padding: 0.5%;
    display: block;
    cursor: pointer;
    transition: width 2s;
    min-width: 295px;
    word-break: normal;
    text-align: right;
  }

  .links {
    text-align: left;
  }

.sort {
    vertical-align: middle;
  }

  @media screen and (max-width: 900px) {
    .words {
      font-size: 14px;
      min-width: 100px;
    }
  }
</style>
