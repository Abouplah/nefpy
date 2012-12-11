(function() {

    $(document).ready(function() {

        $("#btnrechercheavance").click(function() {
            if($("#rechercheavancee").css('display') == 'none') {
                $("#rechercheavancee").show();
            }
            else {
                $("#rechercheavancee").hide();
            }
			return false;
        });

        $("#btninscription").click(function() {
            if($("#inscription").css('display') == 'none') {
                $("#inscription").show();
            }
            else {
                $("#inscription").hide();
            }
			return false;
        });
    });

})();
