<script>
    let menuOpen = false;

    function toggleMenu() {
        menuOpen = !menuOpen;
    }
</script>

<header class="header">
    <div class="title text-3xl md:text-4xl lg:text-5xl flex justify-center items-center">
        <h1>お絵かきランニング</h1>
    </div>

    <!-- ハンバーガーメニューのボタン -->
    <span class="menu-toggle text-6xl flex justify-center items-center relative bottom-1" on:click={toggleMenu} aria-label="Toggle navigation">
        ☰
    </span>
</header>

<style>
    .header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 80px;
        background-color: #174a97;
        color: #ffffff;
        display: flex;
        z-index: 1000;
        box-shadow: 0 4px 10px rgba(5, 81, 188, 0.661);
        justify-content: space-between;
        padding: 0 20px;
    }

    /* ハンバーガーメニューのボタン */
    .menu-toggle {
        display: none; /* PCでは非表示 */
        background: none;
        border: none;
        color: white;
        cursor: pointer;
    }

    @media (max-width: 600px) {
        .menu-toggle {
            display: block; /* スマホで表示 */
        }
    }
</style>
