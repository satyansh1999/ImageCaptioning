var express = require("express"),
app = express(),
parser = require("body-parser"),
sanitize = require("express-sanitizer"),
method_override = require("method-override"),
upload = require('express-fileupload');

// app setup
app.set("view engine","ejs");
app.use(parser.urlencoded({extended:true}));
app.use(express.static("public"));
app.use(sanitize());
app.use(method_override("_method"));
app.use(upload());

textField = "";

app.get("/",function(req,res){
    res.redirect("/imagecap");
});

app.get("/imagecap",function(req,res){
    res.render("index", {text : textField});
});

app.post("/imagecap/caption", function(req,res){
    if(req.files){
        var file = req.files.file;
        var filename = file.name;
        file.mv("./uploads/"+filename,function(err){
            if(err)    textField = "Cannot upload image";
            else{
                // console.log(filename);
                const spawn = require("child_process").spawn;
                const python =  spawn("python3",["./python/trained.py",filename]);
                python.stdout.on('data', function (data) {
                    // console.log(data.toString());
                    // console.log("python");
                    resp = data.toString();
                    myjson = JSON.parse(resp);
                    textField = myjson.desc;
                    // console.log(myjson.desc);
                });
            }
            // console.log("end");
            res.redirect("/imagecap");
        });
    }
    else{
        console.log("Failed to save image");
        res.redirect("/imagecap");
    }
});

app.listen(3000,function(){
    console.log("Serving PicTalk..")
});