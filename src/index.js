import './main.css'

import jquery from "jquery";
window.$ = window.jQuery = jquery;

import Home from "./assets/modules/home";
import Visualisation from "./assets/modules/visualisation";

$(function () {
    Home.init();
    Visualisation.init();
});
