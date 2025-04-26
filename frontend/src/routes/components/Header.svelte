<script>
    let menuOpen = false;

    function toggleMenu() {
        menuOpen = !menuOpen;
    }
</script>

<header class="header">
    <div class="header-logo title text-3xl md:text-4xl lg:text-5xl flex justify-center items-center">
        <img src="./DrawingRunning_logo_strings.png" class="logo">
    </div>
</header>

<style>
    .header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 80px;
        background-color: #000825;
        color: #ffffff;
        display: flex;
        z-index: 1000;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        justify-content: space-between;
        padding: 0 10px;
    }

    .header-logo {
        display: flex;
        align-items: center;                
   }

    .header-logo img {
        margin-top: 3px;
        width: 50%;
        height: auto;
    }

    @media (max-width: 600px) {
        .menu-toggle {
            display: block; /* スマホで表示 */
        }
    }
</style>
